#!/usr/bin/env python3
"""Lint a GOF ontology instance and print a health report (docs/04-extending.md, "Care mode").

Usage:
    python lint_ontology.py <ontology-dir> [--schemas <dir>]

Schemas default to the `schemas/` directory next to this tool's parent
(works both at the repo root and inside the packaged skill). Requires pyyaml;
`jsonschema` is optional -- without it the schema check is skipped with a warning.

If the ontology manifest declares `context_root`, the linked company-context
tree is loaded too: its artifacts are schema-checked, cross-tree references
(product-group:, gtm-motion:, icp:, ...) are resolved, its manifests are
checked for completeness, and freshness checks apply to its artifacts.

Checks (ERROR fails the run, WARN does not):
    parse             artifact file that does not parse as YAML
    schema            artifact does not validate against schemas/<kind>.schema.json
    ref               a kind:id reference that does not resolve
    manifest-missing  artifact on disk not listed in the manifest
    manifest-dangling manifest entry whose path does not exist
    context-root      manifest context_root does not resolve to a context tree
    context-dangling  context manifest entry whose path/id does not exist
    context-unlisted  context artifact not listed in any context manifest
    motion-dup        duplicate motion id across gtm-motions artifacts
    orphan            artifact that nothing references (entry-point kinds excluded)
    prompt-unused     prompt no artifact references
    enum-gap          enum value with definition: null
    draft-ref         confirmed artifact referencing a draft artifact
    overdue           last_verified + verify_every lies in the past
    expired           valid_until lies in the past
    pii               pii: true property without allowed_in_context: false + freshness: live-only
    ai-prompt         filled_by: ai property without a resolvable ai.prompt_ref
    loop-owner        loop without an owner (a loop without a steward does not ship)
    loop-level        loop level outside the ladder, above the agent's cap, or unknown agent
    evidence          source: learned without evidence, or evidence without source: learned

Exit codes: 0 = no errors (warnings allowed), 1 = errors, 2 = usage/IO failure.
"""
import sys, os, re, glob, datetime

try:
    import yaml
except ImportError:
    sys.exit("lint_ontology.py requires pyyaml: pip install pyyaml")

try:
    import jsonschema
except ImportError:
    jsonschema = None

# Keep REF_RE identical to the one in render_ontology.py. Longer kinds must
# precede shorter prefixes of themselves (product-group-strategy before
# product-group, gtm-motions before gtm-motion).
REF_RE = re.compile(
    r"\b(object|process|automation|action|kpi|prompt|draft|system|property|loop|claim"
    r"|product-group-strategy|product-group|gtm-motions|gtm-motion|segment|use-case"
    r"|icp|personas|buying-context|positioning|value-propositions|messaging"
    r"|product-context):([a-z0-9_./=-]+)")
KIND_MAP = {"object": "object-type", "product-group": "product-group-manifest"}
# Kinds nothing is expected to reference: entry points, indexes, and infrastructure.
ORPHAN_EXEMPT = {"manifest", "glossary", "agent-policy", "identity",
                 "discovery-snapshot", "loop", "binding", "prompt"}
# Company-context artifact kinds; all validate against context-artifact.schema.json.
CONTEXT_DOC_KINDS = {"company-profile", "company-strategy", "commercial-model",
                     "operating-model", "market-overview", "competitor-landscape",
                     "product-group-strategy", "segment", "use-case", "icp",
                     "personas", "buying-context", "gtm-motions", "positioning",
                     "value-propositions", "messaging", "product-context"}
CONTEXT_MANIFEST_KINDS = {"company-context-manifest", "product-group-manifest"}
# Documentation files inside a context tree; not artifacts, never linted.
GUIDE_KINDS = {"company-context-readme", "company-context-agent-guide",
               "company-context-artifact-guide"}
PERIOD_DAYS = {"d": 1, "w": 7, "m": 30, "y": 365}


def load(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".md"):
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
        return (yaml.safe_load(m.group(1)) if m else None), text
    return yaml.safe_load(text), text


def coerce(d):
    if isinstance(d, dict):
        return {k: coerce(v) for k, v in d.items()}
    if isinstance(d, list):
        return [coerce(x) for x in d]
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.isoformat()
    return d


def as_date(v):
    if isinstance(v, datetime.datetime):
        return v.date()
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str):
        try:
            return datetime.date.fromisoformat(v.strip())
        except ValueError:
            return None
    return None


class Linter:
    def __init__(self, root, schema_dir):
        self.root = root
        self.schema_dir = schema_dir
        self.findings = []          # (severity, check, relpath, message)
        self.docs, self.raws = {}, {}
        self.tree = {}              # file -> "ontology" | "context"
        self.context_dir = None
        self.today = datetime.date.today()

    def add(self, severity, check, path, message):
        rel = os.path.relpath(path, self.root) if os.path.isabs(path) else path
        self.findings.append((severity, check, rel, message))

    # ------------------------------------------------------------- loading ---
    def collect_tree(self, root, origin):
        for ext in ("yaml", "yml", "md"):
            for f in glob.glob(os.path.join(root, "**", f"*.{ext}"), recursive=True):
                if os.sep + "render" + os.sep in f:
                    continue
                try:
                    d, raw = load(f)
                except Exception as e:
                    self.add("ERROR", "parse", f, str(e))
                    continue
                if isinstance(d, dict) and "kind" in d and d["kind"] not in GUIDE_KINDS:
                    self.docs[f] = d
                    self.raws[f] = raw
                    self.tree[f] = origin

    def collect(self):
        self.collect_tree(self.root, "ontology")

    def collect_context(self):
        """Load the company-context tree the manifest points at via context_root."""
        manifest = next((d for d in self.docs.values() if d.get("kind") == "manifest"), None)
        ctx = (manifest or {}).get("context_root")
        if not ctx:
            return
        ctx_dir = os.path.normpath(os.path.join(self.root, ctx))
        if not os.path.isdir(ctx_dir) or not os.path.exists(os.path.join(ctx_dir, "manifest.yaml")):
            self.add("ERROR", "context-root", ".",
                     f"context_root '{ctx}' does not resolve to a directory with a manifest.yaml")
            return
        self.context_dir = ctx_dir
        self.collect_tree(ctx_dir, "context")

    # ---------------------------------------------------------- reference ----
    def build_refs(self):
        """ids, per-object property index, and resolved edges (src_file, tgt_ref)."""
        self.ids = {f"{d['kind']}:{d['id']}" for d in self.docs.values() if "id" in d}
        self.props = {d["id"]: {p.get("id") for p in d.get("properties", [])}
                      for d in self.docs.values() if d.get("kind") == "object-type"}
        self.by_ref = {f"{d['kind']}:{d['id']}": d for d in self.docs.values() if "id" in d}
        # Motion ids declared in gtm-motions frontmatter are canonical gtm-motion: targets.
        self.motion_owner = {}
        for f, d in sorted(self.docs.items()):
            if d.get("kind") != "gtm-motions":
                continue
            for m in d.get("motions") or []:
                if not isinstance(m, dict) or not m.get("id"):
                    continue
                ref = f"gtm-motion:{m['id']}"
                if ref in self.ids:
                    self.add("ERROR", "motion-dup", f, f"duplicate motion id '{m['id']}'")
                    continue
                self.ids.add(ref)
                self.by_ref[ref] = d
                self.motion_owner[ref] = f"gtm-motions:{d['id']}" if "id" in d else None
        self.claims = {}
        for f, d in sorted(self.docs.items()):
            if d.get("kind") != "claim-registry":
                continue
            for claim in d.get("claims") or []:
                if not isinstance(claim, dict) or not claim.get("id"):
                    continue
                ref = f"claim:{claim['id']}"
                if ref in self.ids:
                    self.add("ERROR", "claim-dup", f, f"duplicate claim id '{claim['id']}'")
                    continue
                self.ids.add(ref)
                self.by_ref[ref] = claim
                self.claims[ref] = (f, claim)
        self.edges = []
        for f, d in self.docs.items():
            src = f"{d['kind']}:{d['id']}" if "id" in d else None
            for kind, rest in REF_RE.findall(self.raws[f]):
                rest = rest.rstrip("./=-")
                if kind == "property":
                    parts = rest.split(".")
                    obj, prop = parts[0], (parts[1] if len(parts) > 1 else None)
                    if obj not in self.props:
                        self.add("ERROR", "ref", f, f"property:{rest} - unknown object '{obj}'")
                    elif prop and prop not in self.props[obj]:
                        self.add("ERROR", "ref", f, f"property:{rest} - object '{obj}' has no property '{prop}'")
                    else:
                        self.edges.append((f, f"object-type:{obj}"))
                    continue
                base = rest.split("/")[0].split(".")[0].split("=")[0]
                tgt = f"{KIND_MAP.get(kind, kind)}:{base}"
                if tgt not in self.ids:
                    self.add("ERROR", "ref", f, f"{kind}:{base} does not resolve")
                elif src != tgt:
                    self.edges.append((f, tgt))
                    owner = self.motion_owner.get(tgt)
                    if owner and owner != src:
                        self.edges.append((f, owner))

    # ------------------------------------------------------------- checks ----
    def check_schema(self):
        if jsonschema is None:
            self.add("WARN", "schema", ".", "schema validation skipped: pip install jsonschema")
            return
        cache = {}
        for f, d in sorted(self.docs.items()):
            name = "context-artifact" if d["kind"] in CONTEXT_DOC_KINDS else d["kind"]
            sf = os.path.join(self.schema_dir, f"{name}.schema.json")
            if not os.path.exists(sf):
                continue
            if sf not in cache:
                import json
                cache[sf] = jsonschema.Draft202012Validator(json.load(open(sf, encoding="utf-8")))
            for e in sorted(cache[sf].iter_errors(coerce(d)), key=lambda e: list(e.absolute_path)):
                where = "/".join(str(p) for p in e.absolute_path) or "(root)"
                self.add("ERROR", "schema", f, f"{where}: {e.message[:200]}")

    def check_manifest(self):
        manifest = next((d for f, d in self.docs.items() if d["kind"] == "manifest"), None)
        mfile = next((f for f, d in self.docs.items() if d["kind"] == "manifest"), None)
        self.manifest = manifest or {}
        if manifest is None:
            self.add("ERROR", "manifest-missing", ".", "no manifest.yaml found")
            return
        listed = {a.get("path") for a in manifest.get("artifacts", [])}
        for p in sorted(listed):
            if p and not os.path.exists(os.path.join(self.root, p)):
                self.add("ERROR", "manifest-dangling", mfile, f"listed artifact does not exist: {p}")
        for f, d in sorted(self.docs.items()):
            if self.tree.get(f) == "context":
                continue
            rel = os.path.relpath(f, self.root)
            if d["kind"] == "manifest":
                continue
            if rel not in listed:
                self.add("ERROR", "manifest-missing", f, "artifact not listed in manifest.yaml")

    def check_context_manifest(self):
        """Completeness of the context tree's own manifests (root + per group)."""
        if not self.context_dir:
            return
        entry = next(((f, d) for f, d in sorted(self.docs.items())
                      if d.get("kind") == "company-context-manifest"), None)
        if entry is None:
            self.add("ERROR", "context-root", self.context_dir,
                     "context tree has no company-context-manifest")
            return
        mfile, m = entry
        listed = set()
        claims_registry = m.get("claims_registry")
        if claims_registry:
            cp = os.path.normpath(os.path.join(self.context_dir, claims_registry))
            if not os.path.exists(cp):
                self.add("ERROR", "context-dangling", mfile,
                         f"claims_registry does not exist: {claims_registry}")
            else:
                cd = next((d for f, d in self.docs.items() if os.path.normpath(f) == cp), None)
                if not cd or cd.get("kind") != "claim-registry":
                    self.add("ERROR", "context-dangling", mfile,
                             f"claims_registry is not a claim-registry: {claims_registry}")
                else:
                    listed.add(cp)
        company_ids = {a.get("id") for a in m.get("artifacts", []) if isinstance(a, dict)}
        for a in m.get("artifacts", []):
            p = os.path.normpath(os.path.join(self.context_dir, a.get("path", "")))
            if not os.path.exists(p):
                self.add("ERROR", "context-dangling", mfile,
                         f"listed artifact does not exist: {a.get('path')}")
            else:
                listed.add(p)
        for g in m.get("product_groups", []):
            gp = os.path.normpath(os.path.join(self.context_dir, g.get("path", "")))
            if not os.path.exists(gp):
                self.add("ERROR", "context-dangling", mfile,
                         f"listed product group does not exist: {g.get('path')}")
                continue
            gd = next((d for f, d in self.docs.items() if os.path.normpath(f) == gp), None)
            if not gd or gd.get("kind") != "product-group-manifest":
                self.add("ERROR", "context-dangling", mfile,
                         f"product group path is not a product-group-manifest: {g.get('path')}")
                continue
            listed.add(gp)
            gdir = os.path.dirname(gp)
            for i in gd.get("inherits") or []:
                if i not in company_ids:
                    self.add("ERROR", "context-dangling", gp,
                             f"inherits '{i}' does not match a company artifact id")
            for a in (gd.get("artifacts") or []) + (gd.get("products") or []):
                p = os.path.normpath(os.path.join(gdir, a.get("path", "")))
                if not os.path.exists(p):
                    self.add("ERROR", "context-dangling", gp,
                             f"listed artifact does not exist: {a.get('path')}")
                else:
                    listed.add(p)
        for f, d in sorted(self.docs.items()):
            if self.tree.get(f) != "context" or d.get("kind") in CONTEXT_MANIFEST_KINDS:
                continue
            if os.path.normpath(f) not in listed:
                self.add("ERROR", "context-unlisted", f,
                         "context artifact not listed in any context manifest")

    def check_orphans(self):
        inbound = {tgt for _, tgt in self.edges}
        for f, d in sorted(self.docs.items()):
            if "id" not in d:
                continue
            # Context artifacts are navigated via manifests + load_when, not the ref graph.
            if self.tree.get(f) == "context":
                continue
            ref = f"{d['kind']}:{d['id']}"
            if d["kind"] == "prompt" and ref not in inbound:
                self.add("WARN", "prompt-unused", f, "prompt is never referenced")
            elif d["kind"] == "kpi" and d.get("level") == "company":
                continue  # company KPIs sit at the top of the tree; nothing above references them
            elif d["kind"] not in ORPHAN_EXEMPT and ref not in inbound:
                self.add("WARN", "orphan", f, "no other artifact references this one")

    def check_draft_refs(self):
        for f, tgt in self.edges:
            src = self.docs[f]
            if (src.get("meta") or {}).get("status") != "confirmed":
                continue
            target = self.by_ref.get(tgt, {})
            target_status = target.get("status") if tgt.startswith("claim:") \
                else (target.get("meta") or {}).get("status")
            if target_status == "draft":
                self.add("ERROR", "draft-ref", f, f"confirmed artifact references draft {tgt}")

    def check_expired_claim_refs(self):
        for f, tgt in self.edges:
            if not tgt.startswith("claim:") or self.docs[f].get("kind") == "claim-registry":
                continue
            valid_until = as_date(self.by_ref.get(tgt, {}).get("valid_until"))
            if valid_until and valid_until < self.today:
                self.add("ERROR", "expired-ref", f, f"artifact references expired {tgt}")

    def metas(self):
        for f, d in sorted(self.docs.items()):
            if d.get("meta"):
                yield f, "artifact", d["meta"]
            for p in d.get("properties", []) if d.get("kind") == "object-type" else []:
                if isinstance(p, dict) and p.get("meta"):
                    yield f, f"property {p.get('id')}", p["meta"]
            for claim in d.get("claims", []) if d.get("kind") == "claim-registry" else []:
                if isinstance(claim, dict):
                    yield f, f"claim {claim.get('id')}", claim

    def check_temporal(self):
        for f, where, meta in self.metas():
            lv, ve = as_date(meta.get("last_verified")), meta.get("verify_every")
            if lv and ve:
                m = re.fullmatch(r"(\d+)([dwmy])", str(ve))
                if m:
                    due = lv + datetime.timedelta(days=int(m.group(1)) * PERIOD_DAYS[m.group(2)])
                    if due < self.today:
                        self.add("WARN", "overdue", f,
                                 f"{where}: last_verified {lv} + verify_every {ve} - overdue since {due}")
            vu = as_date(meta.get("valid_until"))
            if vu and vu < self.today and not where.startswith("claim "):
                self.add("ERROR", "expired", f, f"{where}: valid_until {vu} has passed")

    def check_evidence(self):
        for f, where, meta in self.metas():
            if where.startswith("claim "):
                continue
            if meta.get("source") == "learned" and not meta.get("evidence"):
                self.add("WARN", "evidence", f, f"{where}: source: learned without evidence")
            if meta.get("evidence") and meta.get("source") != "learned":
                self.add("WARN", "evidence", f, f"{where}: evidence given but source is not 'learned'")

    def check_claims(self):
        for ref, (f, claim) in sorted(self.claims.items()):
            evidence = claim.get("evidence") or []
            evidence_ids = [item.get("id") for item in evidence if isinstance(item, dict)]
            if len(evidence_ids) != len(set(evidence_ids)):
                self.add("ERROR", "claim-evidence", f, f"{ref} has duplicate evidence ids")
            if claim.get("status") in {"confirmed", "example"} and not any(
                isinstance(item, dict) and item.get("relation") == "supports" for item in evidence
            ):
                self.add("ERROR", "claim-evidence", f, f"{ref} has no supporting evidence")
            start, end = as_date(claim.get("valid_from")), as_date(claim.get("valid_until"))
            if start and end and start > end:
                self.add("ERROR", "claim-temporal", f, f"{ref} valid_from is after valid_until")
            for field in ("conflicts_with", "supersedes"):
                for target in claim.get(field) or []:
                    if target == ref:
                        self.add("ERROR", "claim-ref", f, f"{ref}.{field} references itself")
                    elif claim.get("status") == "confirmed" and \
                            (self.by_ref.get(target) or {}).get("status") == "draft":
                        self.add("ERROR", "draft-ref", f, f"confirmed {ref}.{field} references draft {target}")
            for target in claim.get("conflicts_with") or []:
                other = self.by_ref.get(target) or {}
                if ref not in (other.get("conflicts_with") or []):
                    self.add("ERROR", "claim-conflict", f,
                             f"{ref} conflict with {target} is not reciprocal")

    def check_properties(self):
        for f, d in sorted(self.docs.items()):
            if d.get("kind") != "object-type":
                continue
            for p in d.get("properties", []):
                if not isinstance(p, dict):
                    continue
                pid = p.get("id")
                if p.get("pii") is True and not (p.get("allowed_in_context") is False
                                                 and p.get("freshness") == "live-only"):
                    self.add("ERROR", "pii", f,
                             f"property {pid}: pii: true requires allowed_in_context: false and freshness: live-only")
                if p.get("filled_by") == "ai":
                    pref = (p.get("ai") or {}).get("prompt_ref")
                    if not pref or pref not in self.ids:
                        self.add("ERROR", "ai-prompt", f,
                                 f"property {pid}: filled_by: ai without a resolvable ai.prompt_ref")
                for v in p.get("enum") or []:
                    if isinstance(v, dict) and v.get("definition") is None:
                        self.add("WARN", "enum-gap", f,
                                 f"property {pid}: enum value '{v.get('value')}' has definition: null")

    def check_action_contexts(self):
        property_defs = {}
        for d in self.docs.values():
            if d.get("kind") != "object-type":
                continue
            for prop in d.get("properties") or []:
                if isinstance(prop, dict) and prop.get("id"):
                    property_defs[f"property:{d['id']}.{prop['id']}"] = prop

        for f, action in sorted(self.docs.items()):
            if action.get("kind") != "action":
                continue
            meta = action.get("meta") or {}
            context = action.get("context")
            if not context:
                if meta.get("status") == "confirmed" and action.get("executor") in {"agent", "either"}:
                    self.add("WARN", "action-context", f,
                             "confirmed agent/either action has no context contract")
                continue

            input_ids = {item.get("id") for item in action.get("inputs") or []
                         if isinstance(item, dict) and item.get("id")}
            protected = set(context.get("forbidden_to_persist") or [])
            for ref in protected:
                if ref.startswith("input:") and ref.removeprefix("input:") not in input_ids:
                    self.add("ERROR", "action-context", f,
                             f"forbidden_to_persist references unknown {ref}")

            for ref in context.get("required_live_refs") or []:
                prop = property_defs.get(ref)
                if prop is None:
                    self.add("ERROR", "action-context", f,
                             f"required_live_refs contains unknown {ref}")
                    continue
                if (prop.get("pii") is True or prop.get("freshness") == "live-only") \
                        and ref not in protected:
                    self.add("ERROR", "action-context", f,
                             f"{ref} is pii/live-only and must be in forbidden_to_persist")

    def check_loops(self):
        loops = [(f, d) for f, d in sorted(self.docs.items()) if d.get("kind") == "loop"]
        if not loops:
            return
        policy = next((d for d in self.docs.values() if d.get("kind") == "agent-policy"), None)
        if policy is None:
            for f, _ in loops:
                self.add("ERROR", "loop-level", f, "no agent-policy to validate loop levels against")
            return
        ladder = policy.get("permission_ladder") or {}
        levels = {l.get("level") for l in ladder.get("levels", []) if isinstance(l, dict)}
        caps = {a.get("id"): a.get("max_permission_level")
                for a in policy.get("agents", []) if isinstance(a, dict)}
        for f, d in loops:
            if not str(d.get("owner") or "").strip():
                self.add("ERROR", "loop-owner", f, "loop has no owner (steward)")
            for field in ("permission_level", "target_level"):
                lvl = d.get(field)
                if lvl is not None and lvl not in levels:
                    self.add("ERROR", "loop-level", f,
                             f"{field} {lvl} is not a level defined in the agent-policy ladder")
            agent = d.get("agent")
            if agent is not None:
                if agent not in caps:
                    self.add("ERROR", "loop-level", f, f"agent '{agent}' is not defined in agent-policy")
                elif caps[agent] is not None and isinstance(d.get("permission_level"), int) \
                        and d["permission_level"] > caps[agent]:
                    self.add("ERROR", "loop-level", f,
                             f"permission_level {d['permission_level']} exceeds "
                             f"agent '{agent}' max_permission_level {caps[agent]}")

    # -------------------------------------------------------------- report ---
    def report(self):
        errors = sorted(x for x in self.findings if x[0] == "ERROR")
        warns = sorted(x for x in self.findings if x[0] == "WARN")
        name = self.manifest.get("ontology", "?")
        version = self.manifest.get("version", "?")
        print(f"GOF health report: {name} {version} ({os.path.basename(os.path.abspath(self.root))})")
        for title, rows in (("ERRORS", errors), ("WARNINGS", warns)):
            if rows:
                print(f"\n{title} ({len(rows)})")
                for _, check, rel, msg in rows:
                    print(f"  [{check}] {rel}: {msg}")
        print(f"\n{len(errors)} error{'s' if len(errors) != 1 else ''}, "
              f"{len(warns)} warning{'s' if len(warns) != 1 else ''}.")
        return 1 if errors else 0

    def run(self):
        self.collect()
        if not self.docs:
            print(f"no ontology artifacts found under {self.root}", file=sys.stderr)
            return 2
        self.collect_context()
        self.build_refs()
        self.check_schema()
        self.check_manifest()
        self.check_context_manifest()
        self.check_orphans()
        self.check_draft_refs()
        self.check_expired_claim_refs()
        self.check_temporal()
        self.check_evidence()
        self.check_claims()
        self.check_properties()
        self.check_action_contexts()
        self.check_loops()
        return self.report()


def main():
    args = [a for a in sys.argv[1:]]
    schema_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas")
    if "--schemas" in args:
        i = args.index("--schemas")
        try:
            schema_dir = args[i + 1]
        except IndexError:
            sys.exit(__doc__)
        del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    root = args[0].rstrip("/")
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    if not os.path.isdir(schema_dir):
        print(f"schemas directory not found: {schema_dir} (use --schemas)", file=sys.stderr)
        return 2
    return Linter(root, schema_dir).run()


if __name__ == "__main__":
    sys.exit(main())
