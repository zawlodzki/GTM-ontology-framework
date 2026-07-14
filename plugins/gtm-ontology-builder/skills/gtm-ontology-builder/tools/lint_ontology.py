#!/usr/bin/env python3
"""Lint a GOF ontology instance and print a health report (docs/04-extending.md, "Care mode").

Usage:
    python lint_ontology.py <ontology-dir> [--schemas <dir>]

Schemas default to the `schemas/` directory next to this tool's parent
(works both at the repo root and inside the packaged skill). Requires pyyaml;
`jsonschema` is optional -- without it the schema check is skipped with a warning.

Checks (ERROR fails the run, WARN does not):
    parse             artifact file that does not parse as YAML
    schema            artifact does not validate against schemas/<kind>.schema.json
    ref               a kind:id reference that does not resolve
    manifest-missing  artifact on disk not listed in the manifest
    manifest-dangling manifest entry whose path does not exist
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

REF_RE = re.compile(r"\b(object|process|automation|action|kpi|prompt|draft|system|property|loop):([a-z0-9_./=-]+)")
KIND_MAP = {"object": "object-type"}
# Kinds nothing is expected to reference: entry points, indexes, and infrastructure.
ORPHAN_EXEMPT = {"manifest", "business-context", "glossary", "agent-policy", "identity",
                 "discovery-snapshot", "loop", "binding", "prompt"}
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
        self.today = datetime.date.today()

    def add(self, severity, check, path, message):
        rel = os.path.relpath(path, self.root) if os.path.isabs(path) else path
        self.findings.append((severity, check, rel, message))

    # ------------------------------------------------------------- loading ---
    def collect(self):
        for ext in ("yaml", "yml", "md"):
            for f in glob.glob(os.path.join(self.root, "**", f"*.{ext}"), recursive=True):
                if os.sep + "render" + os.sep in f:
                    continue
                try:
                    d, raw = load(f)
                except Exception as e:
                    self.add("ERROR", "parse", f, str(e))
                    continue
                if isinstance(d, dict) and "kind" in d:
                    self.docs[f] = d
                    self.raws[f] = raw

    # ---------------------------------------------------------- reference ----
    def build_refs(self):
        """ids, per-object property index, and resolved edges (src_file, tgt_ref)."""
        self.ids = {f"{d['kind']}:{d['id']}" for d in self.docs.values() if "id" in d}
        self.props = {d["id"]: {p.get("id") for p in d.get("properties", [])}
                      for d in self.docs.values() if d.get("kind") == "object-type"}
        self.by_ref = {f"{d['kind']}:{d['id']}": d for d in self.docs.values() if "id" in d}
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

    # ------------------------------------------------------------- checks ----
    def check_schema(self):
        if jsonschema is None:
            self.add("WARN", "schema", ".", "schema validation skipped: pip install jsonschema")
            return
        cache = {}
        for f, d in sorted(self.docs.items()):
            sf = os.path.join(self.schema_dir, f"{d['kind']}.schema.json")
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
            rel = os.path.relpath(f, self.root)
            if d["kind"] == "manifest":
                continue
            if rel not in listed:
                self.add("ERROR", "manifest-missing", f, "artifact not listed in manifest.yaml")

    def check_orphans(self):
        inbound = {tgt for _, tgt in self.edges}
        for f, d in sorted(self.docs.items()):
            if "id" not in d:
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
            if (self.by_ref.get(tgt, {}).get("meta") or {}).get("status") == "draft":
                self.add("ERROR", "draft-ref", f, f"confirmed artifact references draft {tgt}")

    def metas(self):
        for f, d in sorted(self.docs.items()):
            if d.get("meta"):
                yield f, "artifact", d["meta"]
            for p in d.get("properties", []) if d.get("kind") == "object-type" else []:
                if isinstance(p, dict) and p.get("meta"):
                    yield f, f"property {p.get('id')}", p["meta"]

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
            if vu and vu < self.today:
                self.add("ERROR", "expired", f, f"{where}: valid_until {vu} has passed")

    def check_evidence(self):
        for f, where, meta in self.metas():
            if meta.get("source") == "learned" and not meta.get("evidence"):
                self.add("WARN", "evidence", f, f"{where}: source: learned without evidence")
            if meta.get("evidence") and meta.get("source") != "learned":
                self.add("WARN", "evidence", f, f"{where}: evidence given but source is not 'learned'")

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
        self.build_refs()
        self.check_schema()
        self.check_manifest()
        self.check_orphans()
        self.check_draft_refs()
        self.check_temporal()
        self.check_evidence()
        self.check_properties()
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
