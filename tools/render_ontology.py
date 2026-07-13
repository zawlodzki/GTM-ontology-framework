#!/usr/bin/env python3
"""Render a GOF ontology instance into human-facing views (docs/06-human-render.md).

Usage:
    python render_ontology.py <ontology-dir> [out-dir]

Outputs (default out-dir: <ontology-dir>/render):
    process-<id>.md   human-readable table (columns = stages) + Mermaid funnel diagram
    fields.md         field dictionary per object (no field keys, no YAML)
    actions.md        agent action catalog
    graph.md          Mermaid graph of artifacts and their references
    explorer.html     self-contained interactive explorer (funnel, objects,
                      actions, automations, KPIs, reference graph)

Renders are GENERATED; never hand-edit, regenerate after each version bump.
"""
import sys, os, re, json, glob, datetime
from collections import defaultdict

import yaml

REF_RE = re.compile(r"\b(object|process|automation|action|kpi|prompt|draft|system|property):([a-z0-9_./=-]+)")


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


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", "<br>").strip()


def collect(root):
    docs, raws = {}, {}
    for ext in ("yaml", "yml", "md"):
        for f in glob.glob(os.path.join(root, "**", f"*.{ext}"), recursive=True):
            if os.sep + "render" + os.sep in f:
                continue
            try:
                d, raw = load(f)
            except Exception as e:
                print(f"warn: cannot parse {f}: {e}", file=sys.stderr)
                continue
            if isinstance(d, dict) and "kind" in d:
                docs[f] = coerce(d)
                raws[f] = raw
    return docs, raws


# ---------------------------------------------------------------- process ----
STAGE_ROWS = [
    ("Definition",        lambda s: s.get("definition", "")),
    ("Entry criteria",    lambda s: "; ".join(c["description"] for c in s.get("entry_criteria", []))),
    ("Exit criteria",     lambda s: "; ".join(c["description"] for c in s.get("exit_criteria", []))),
    ("NOT enough (bad examples)", lambda s: "; ".join(s.get("bad_examples", []))),
    ("Customer verifier", lambda s: (s.get("customer_verifier") or {}).get("description", "")),
    ("Probability",       lambda s: "" if s.get("probability") is None else f"{int(round(s['probability']*100))}%"),
    ("Required fields",   lambda s: ", ".join(s.get("required_properties", []))),
    ("Mandatory tasks",   lambda s: "; ".join((s.get("tasks") or {}).get("mandatory", []))),
    ("SLA (target / rotting)", lambda s: " / ".join(str((s.get("sla") or {}).get(k, "n/a"))
                              for k in ("target_duration_days", "rotting_threshold_days")) if s.get("sla") else ""),
    ("Owner",             lambda s: s.get("owner_role", "")),
    ("Automations",       lambda s: ", ".join(a.split(":", 1)[1] for a in s.get("automations_triggered", []))),
    ("KPIs",              lambda s: ", ".join(k.split(":", 1)[1] for k in s.get("kpis", []))),
    ("Loss reasons",      lambda s: "; ".join(s.get("loss_reasons", []))),
    ("Tips",              lambda s: s.get("tips", "")),
]


def mermaid_funnel(proc):
    stages = sorted(proc["stages"], key=lambda s: s["order"])
    lines = ["```mermaid", "flowchart LR"]
    for s in stages:
        p = "" if s.get("probability") is None else f"<br/>p={int(round(s['probability']*100))}%"
        node = f'{s["id"]}["{s["name"]}{p}"]'
        lines.append(f"  {node}")
    for frm, to in proc.get("transitions", {}).get("allowed", []):
        tgt = next((s for s in stages if s["id"] == to), {})
        arrow = "-.->" if tgt.get("outcome") == "negative" else "-->"
        lines.append(f"  {frm} {arrow} {to}")
    for s in stages:
        if s.get("terminal"):
            color = "#1a7f37" if s.get("outcome") == "positive" else "#b42318"
            lines.append(f"  style {s['id']} fill:{color},color:#fff")
    lines.append("```")
    return "\n".join(lines)


def render_process(proc, meta_line):
    stages = sorted(proc["stages"], key=lambda s: s["order"])
    out = [f"# {proc['name']}", "", proc.get("description", "").strip(), "",
           mermaid_funnel(proc), ""]
    header = "| | " + " | ".join(s["name"] for s in stages) + " |"
    sep = "|---" * (len(stages) + 1) + "|"
    out += [header, sep]
    for label, fn in STAGE_ROWS:
        cells = [esc(fn(s)) for s in stages]
        if not any(cells):
            continue
        out.append(f"| **{label}** | " + " | ".join(cells) + " |")
    out += ["", meta_line, ""]
    return "\n".join(out)


# ----------------------------------------------------------------- fields ----
def render_fields(objects, meta_line):
    out = ["# Field dictionary", ""]
    for o in objects:
        out += [f"## {o['name']}", "", o.get("description", "").strip(), "",
                "| Field | Type | Required | Filled by | Values |", "|---|---|---|---|---|"]
        for p in o.get("properties", []):
            req = p.get("required", "")
            if isinstance(req, dict):
                req = "from stage " + req.get("from_stage", "").split("/")[-1]
            vals = ""
            if p.get("enum"):
                vals = "<br>".join(f"**{v.get('label', v['value'])}**: {esc(v.get('definition') or '(definition pending)')}"
                                   for v in p["enum"])
            out.append(f"| **{p['name']}** | {p['type']} | {req or ''} | {p.get('filled_by','')} | {vals} |")
        out.append("")
    out += [meta_line, ""]
    return "\n".join(out)


# ----------------------------------------------------------------- actions ---
def render_actions(actions, meta_line):
    out = ["# Agent actions", ""]
    for a in actions:
        out += [f"## {a['name']} (`{a['id']}`)", "",
                f"*Executor:* {a['executor']} · *Approval:* {a['approval']}"
                + (f" ({a.get('approval_condition')})" if a.get("approval_condition") else ""), "",
                a.get("intent", "").strip(), "", "**Preconditions**", ""]
        out += [f"1. {p['description']}" for p in a.get("preconditions", [])]
        out += ["", "**Workflow**", ""]
        out += [f"{w.get('step', i+1)}. {w['description']}" for i, w in enumerate(a.get("workflow", []))]
        se = a.get("side_effects", [])
        out += ["", "**Side effects:** " + ("; ".join(se) if se else "none"), ""]
    out += [meta_line, ""]
    return "\n".join(out)


# ------------------------------------------------------------------- graph ---
def build_edges(docs, raws):
    ids = {f"{d['kind']}:{d['id']}" for d in docs.values() if "id" in d}
    prop_owner = {d["id"]: f"object-type:{d['id']}" for d in docs.values() if d["kind"] == "object-type"}
    edges, nodes = set(), {}
    KIND_MAP = {"object": "object-type"}
    for f, d in docs.items():
        if "id" not in d:
            continue
        src = f"{d['kind']}:{d['id']}"
        nodes[src] = d["kind"]
        for kind, rest in REF_RE.findall(raws[f]):
            base = rest.split("/")[0].split(".")[0].split("=")[0]
            if kind == "property":
                tgt = prop_owner.get(base)
            else:
                tgt = f"{KIND_MAP.get(kind, kind)}:{base}"
            if tgt and tgt != src and tgt in ids:
                edges.add((src, tgt))
                nodes.setdefault(tgt, tgt.split(":")[0])
    return nodes, sorted(edges)


def render_graph(nodes, edges, meta_line):
    def nid(ref):
        return ref.replace(":", "_").replace("-", "_")
    out = ["# Artifact reference graph", "", "```mermaid", "flowchart TD"]
    for ref, kind in sorted(nodes.items()):
        label = ref.split(":", 1)[1]
        out.append(f'  {nid(ref)}["{kind}<br/><b>{label}</b>"]')
    for s, t in edges:
        out.append(f"  {nid(s)} --> {nid(t)}")
    out += ["```", "", meta_line, ""]
    return "\n".join(out)


# ---------------------------------------------------------------- explorer ---
HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>GOF Explorer: %%TITLE%%</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/standalone/umd/vis-network.min.js"></script>
<style>
 body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1f2328;background:#f6f8fa}
 header{background:#fff;border-bottom:1px solid #d0d7de;padding:14px 22px}
 header h1{margin:0;font-size:18px} header p{margin:4px 0 0;color:#57606a;max-width:900px}
 nav{display:flex;gap:6px;padding:10px 22px;background:#fff;border-bottom:1px solid #d0d7de;position:sticky;top:0}
 nav button{border:1px solid #d0d7de;background:#f6f8fa;border-radius:6px;padding:6px 14px;cursor:pointer;font-size:13px}
 nav button.on{background:#0969da;color:#fff;border-color:#0969da}
 main{padding:20px 22px;max-width:1200px}
 .cards{display:flex;gap:8px;flex-wrap:wrap;align-items:stretch}
 .stage{border:1px solid #d0d7de;border-radius:8px;background:#fff;padding:10px 12px;min-width:130px;cursor:pointer;flex:1}
 .stage.on{outline:2px solid #0969da}
 .stage.win{border-color:#1a7f37;background:#f0fff4}.stage.loss{border-color:#b42318;background:#fff5f5}
 .bar{height:6px;background:#eaeef2;border-radius:3px;margin-top:6px}.bar i{display:block;height:6px;border-radius:3px;background:#0969da}
 .muted{color:#57606a;font-size:12px}
 .panel,.card{border:1px solid #d0d7de;border-radius:8px;background:#fff;padding:14px 18px;margin-top:14px}
 .badge{display:inline-block;border-radius:10px;padding:1px 9px;font-size:11px;margin-left:6px;color:#fff}
 .b-none{background:#1a7f37}.b-conditional{background:#9a6700}.b-required{background:#b42318}
 .b-human{background:#0969da}.b-automation{background:#8250df}.b-ai{background:#bf3989}.b-integration{background:#1b7c83}.b-mixed{background:#57606a}.b-system{background:#57606a}
 table{border-collapse:collapse;width:100%;background:#fff}th,td{border:1px solid #d0d7de;padding:6px 10px;text-align:left;vertical-align:top}
 th{background:#f6f8fa} h2{font-size:16px;margin:22px 0 8px} h3{font-size:14px;margin:0 0 4px}
 ul{margin:4px 0;padding-left:20px} .neg li{color:#b42318} pre{background:#f6f8fa;padding:8px;border-radius:6px;white-space:pre-wrap;font-size:12px}
 #net{height:560px;border:1px solid #d0d7de;border-radius:8px;background:#fff}
 details{margin:2px 0} summary{cursor:pointer}
 footer{padding:14px 22px;color:#57606a;font-size:12px}
</style></head><body>
<header><h1>%%TITLE%% <span class="muted">v%%VERSION%%</span></h1><p>%%SUMMARY%%</p></header>
<nav id="nav"></nav><main id="main"></main>
<footer>Generated by GOF render_ontology.py, do not hand-edit. Source of truth: the ontology YAML.</footer>
<script>
const D = %%DATA%%;
const TABS = ["Funnel","Objects","Actions","Automations","KPIs","Graph"];
const nav = document.getElementById("nav"), main = document.getElementById("main");
TABS.forEach((t,i)=>{const b=document.createElement("button");b.textContent=t;b.onclick=()=>show(t);nav.appendChild(b);});
function setOn(t){[...nav.children].forEach(b=>b.classList.toggle("on",b.textContent===t));}
const badge=(v,p)=>`<span class="badge b-${v}">${v}</span>`;
const li=xs=>(xs||[]).map(x=>`<li>${x}</li>`).join("");

function show(tab){setOn(tab);main.innerHTML="";({Funnel:funnel,Objects:objects,Actions:actions,Automations:autos,KPIs:kpis,Graph:graph})[tab]();}

function funnel(){
 D.processes.forEach(p=>{
  const h=document.createElement("div");
  h.innerHTML=`<h2>${p.name}</h2><div class="muted">${p.description||""}</div>`;
  const row=document.createElement("div");row.className="cards";
  const panel=document.createElement("div");panel.className="panel";panel.textContent="Click a stage to see its business logic.";
  p.stages.forEach(s=>{
   const c=document.createElement("div");
   c.className="stage"+(s.terminal?(s.outcome==="positive"?" win":" loss"):"");
   const pr=s.probability==null?"":Math.round(s.probability*100)+"%";
   c.innerHTML=`<b>${s.name}</b><div class="muted">${s.owner_role||""}</div>
     <div class="bar"><i style="width:${s.probability!=null?s.probability*100:0}%"></i></div><div class="muted">${pr}</div>`;
   c.onclick=()=>{[...row.children].forEach(x=>x.classList.remove("on"));c.classList.add("on");panel.innerHTML=stageDetail(s);};
   row.appendChild(c);
  });
  main.append(h,row,panel);
 });
}
function stageDetail(s){
 const sla=s.sla?`target ${s.sla.target_duration_days??"n/a"} d · rotting after ${s.sla.rotting_threshold_days??"n/a"} d`:"";
 return `<h3>${s.name}</h3><p>${s.definition||""}</p>
  <b>Entry criteria</b><ul>${li((s.entry_criteria||[]).map(c=>c.description))}</ul>
  <b>Exit criteria</b><ul>${li((s.exit_criteria||[]).map(c=>c.description))}</ul>
  ${s.bad_examples?`<b>NOT enough</b><ul class="neg">${li(s.bad_examples)}</ul>`:""}
  ${s.customer_verifier?`<b>Customer verifier:</b> ${s.customer_verifier.description}<br>`:""}
  ${s.required_properties?`<b>Required fields:</b> ${s.required_properties.join(", ")}<br>`:""}
  ${s.tasks?`<b>Tasks:</b> ${(s.tasks.mandatory||[]).join("; ")}<br>`:""}
  ${sla?`<b>SLA:</b> ${sla}<br>`:""}
  ${s.automations_triggered&&s.automations_triggered.length?`<b>Automations:</b> ${s.automations_triggered.join(", ")}<br>`:""}
  ${s.loss_reasons?`<b>Loss reasons:</b> ${s.loss_reasons.join("; ")}<br>`:""}
  ${s.tips?`<b>Tip:</b> ${s.tips}`:""}`;
}
function objects(){
 D.objects.forEach(o=>{
  const div=document.createElement("div");div.className="card";
  let rows=o.properties.map(p=>{
   let req=p.required===true?"yes":(p.required&&p.required.from_stage?("from "+p.required.from_stage.split("/").pop()):"");
   let vals=(p.enum||[]).map(v=>`<details><summary><b>${v.label||v.value}</b></summary>${v.definition||"(definition pending)"}</details>`).join("");
   if(p.ai)vals+=`<div class="muted">AI field, prompt: ${p.ai.prompt_ref}</div>`;
   return `<tr><td><b>${p.name}</b><div class="muted">${p.semantics||""}</div></td><td>${p.type}</td><td>${req}</td><td>${badge(p.filled_by)}</td><td>${vals}</td></tr>`;
  }).join("");
  div.innerHTML=`<h3>${o.name}</h3><p class="muted">${o.description||""}</p>
   <table><tr><th>Field</th><th>Type</th><th>Required</th><th>Filled by</th><th>Values / notes</th></tr>${rows}</table>`;
  main.appendChild(div);
 });
}
function actions(){
 D.actions.forEach(a=>{
  const div=document.createElement("div");div.className="card";
  div.innerHTML=`<h3>${a.name} ${badge(a.approval)}</h3><p class="muted">${a.intent||a.description||""}</p>
   <b>Preconditions</b><ul>${li((a.preconditions||[]).map(p=>p.description))}</ul>
   <b>Workflow</b><ol>${li((a.workflow||[]).map(w=>w.description))}</ol>
   <b>Side effects:</b> ${(a.side_effects||[]).join("; ")||"none"}<br>
   <b>Implementation:</b> ${(a.implementations||[]).map(i=>`${i.system} via ${i.via} → ${i.tool_or_endpoint}`).join("; ")}`;
  main.appendChild(div);
 });
}
function autos(){
 D.automations.forEach(a=>{
  const fp=a.data_fingerprint||{};
  const div=document.createElement("div");div.className="card";
  div.innerHTML=`<h3>${a.name} <span class="muted">(${a.platform}, ${a.status_live})</span></h3>
   <p class="muted">${a.description||""}</p>
   <b>Trigger:</b> ${a.trigger.event}<br>
   <b>Effects</b><ul>${li((a.effects||[]).map(e=>`${e.operation} → ${e.target}${e.detail?": "+e.detail:""}`))}</ul>
   <b>Fingerprint</b><pre>${Object.entries(fp).map(([k,v])=>k+": "+(Array.isArray(v)?v.join(" | "):v)).join("\\n")}</pre>
   ${a.failure_modes?`<b>Failure modes</b><ul class="neg">${li(a.failure_modes.map(f=>f.symptom+" → "+(f.impact||"")))}</ul>`:""}`;
  main.appendChild(div);
 });
}
function kpis(){
 const div=document.createElement("div");div.className="card";
 div.innerHTML=`<table><tr><th>KPI</th><th>Level</th><th>Formula</th><th>Grain</th><th>Target</th><th>Owner</th></tr>`+
  D.kpis.map(k=>`<tr><td><b>${k.name}</b><div class="muted">${k.definition||""}</div></td><td>${k.level}${k.scope?"<br><span class=muted>"+k.scope+"</span>":""}</td><td><code>${k.formula}</code></td><td>${k.grain}</td><td>${k.target?(k.target.operator+" "+k.target.value+" "+(k.target.unit||"")):""}</td><td>${k.owner}</td></tr>`).join("")+`</table>`;
 main.appendChild(div);
}
const COLORS={"object-type":"#0969da",process:"#1a7f37",automation:"#8250df",action:"#bf3989","kpi":"#9a6700",prompt:"#1b7c83",draft:"#57606a",system:"#24292f",binding:"#d0d7de","agent-policy":"#b42318"};
function graph(){
 const div=document.createElement("div");div.id="net";main.appendChild(div);
 const nodes=D.graph.nodes.map(n=>({id:n.id,label:n.id.split(":")[1],title:n.id,color:COLORS[n.kind]||"#57606a",font:{color:"#fff"},shape:"box"}));
 const edges=D.graph.edges.map(e=>({from:e[0],to:e[1],arrows:"to",color:"#8c959f"}));
 new vis.Network(div,{nodes,edges},{physics:{solver:"forceAtlas2Based",stabilization:{iterations:200}}});
 const leg=document.createElement("div");leg.className="muted";
 leg.innerHTML=Object.entries(COLORS).map(([k,c])=>`<span class="badge" style="background:${c}">${k}</span>`).join(" ");
 main.appendChild(leg);
}
show("Funnel");
</script></body></html>"""


def build_explorer(docs, nodes, edges, manifest):
    by = lambda kind: sorted([d for d in docs.values() if d["kind"] == kind], key=lambda x: x["id"])
    processes = []
    for p in by("process"):
        q = dict(p)
        q["stages"] = sorted(p["stages"], key=lambda s: s["order"])
        processes.append(q)
    data = {
        "objects": by("object-type"),
        "processes": processes,
        "actions": by("action"),
        "automations": by("automation"),
        "kpis": by("kpi"),
        "graph": {"nodes": [{"id": r, "kind": k} for r, k in sorted(nodes.items())],
                  "edges": [list(e) for e in edges]},
    }
    html = (HTML.replace("%%TITLE%%", manifest.get("ontology", "ontology"))
                .replace("%%VERSION%%", str(manifest.get("version", "")))
                .replace("%%SUMMARY%%", str(manifest.get("business_summary", "")).strip())
                .replace("%%DATA%%", json.dumps(data, ensure_ascii=False)))
    return html


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1].rstrip("/")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "render")
    os.makedirs(out, exist_ok=True)

    docs, raws = collect(root)
    manifest = next((d for d in docs.values() if d["kind"] == "manifest"), {})
    meta_line = (f"*Generated from ontology `{manifest.get('ontology','?')}` "
                 f"v{manifest.get('version','?')} ({manifest.get('updated','')}), do not hand-edit.*")

    written = []
    for p in [d for d in docs.values() if d["kind"] == "process"]:
        f = os.path.join(out, f"process-{p['id']}.md")
        open(f, "w", encoding="utf-8").write(render_process(p, meta_line))
        written.append(f)

    objs = sorted([d for d in docs.values() if d["kind"] == "object-type"], key=lambda x: x["id"])
    open(os.path.join(out, "fields.md"), "w", encoding="utf-8").write(render_fields(objs, meta_line))
    acts = sorted([d for d in docs.values() if d["kind"] == "action"], key=lambda x: x["id"])
    open(os.path.join(out, "actions.md"), "w", encoding="utf-8").write(render_actions(acts, meta_line))

    nodes, edges = build_edges(docs, raws)
    open(os.path.join(out, "graph.md"), "w", encoding="utf-8").write(render_graph(nodes, edges, meta_line))
    open(os.path.join(out, "explorer.html"), "w", encoding="utf-8").write(build_explorer(docs, nodes, edges, manifest))
    written += [os.path.join(out, x) for x in ("fields.md", "actions.md", "graph.md", "explorer.html")]
    print("\n".join(os.path.relpath(w) for w in written))


if __name__ == "__main__":
    main()
