#!/usr/bin/env python3
"""Build 4 interactive single-file HTML visuals from data/viz/*.json specs."""
import json, html, math, os

WD = "/home/user/claude-/legal-war-room"
V = f"{WD}/visuals"
os.makedirs(V, exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)

# validated palette (dataviz reference instance) + legal-ledger chrome
BASE_CSS = """
:root{--paper:#FBFAF7;--ink:#23262B;--ink2:#565B63;--line:#DDD8CC;--card:#FFF;
 --navy:#1F3A5F;--maroon:#8E2C2C;--maroon-soft:#F6E9E7;
 --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4;--s7:#4a3aa7;
 --good:#008300;--warn:#c07000;--crit:#e34948;}
@media (prefers-color-scheme: dark){:root:where(:not([data-theme="light"])){
 --paper:#15171B;--ink:#E6E3DA;--ink2:#A9ADB6;--line:#33373E;--card:#1C1F25;
 --navy:#8FB0D8;--maroon:#D98A80;--maroon-soft:#3A2422;
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s7:#9085e9;
 --good:#4fae4f;--warn:#d89a3d;--crit:#e66767;}}
:root[data-theme="dark"]{
 --paper:#15171B;--ink:#E6E3DA;--ink2:#A9ADB6;--line:#33373E;--card:#1C1F25;
 --navy:#8FB0D8;--maroon:#D98A80;--maroon-soft:#3A2422;
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s7:#9085e9;
 --good:#4fae4f;--warn:#d89a3d;--crit:#e66767;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:14.5px/1.5 "Segoe UI",system-ui,sans-serif}
h1{font-family:"Palatino Linotype",Palatino,Georgia,serif;color:var(--navy);font-size:21px;margin:0 0 2px;text-wrap:balance}
.sub{color:var(--ink2);font-size:12.5px;max-width:90ch}
.banner{background:var(--maroon);color:#FBF6F0;text-align:center;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px}
.wrap{max-width:1060px;margin:0 auto;padding:18px 20px 70px}
.num{font-family:ui-monospace,Consolas,monospace;font-variant-numeric:tabular-nums}
.chip{display:inline-block;border:1px solid var(--c,var(--ink2));color:var(--c,var(--ink2));border-radius:11px;padding:0 9px;font-size:11px;max-width:100%;overflow-wrap:break-word}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 15px;margin:10px 0}
table{border-collapse:collapse;width:100%;font-size:12.5px;margin:8px 0}
th{background:var(--navy);color:var(--paper);text-align:left;padding:6px 8px}
td{border:1px solid var(--line);padding:5px 8px;vertical-align:top}
.tbox{overflow-x:auto}
#tip{position:fixed;pointer-events:none;background:var(--card);border:1px solid var(--navy);border-radius:6px;
 padding:8px 11px;font-size:12px;max-width:330px;opacity:0;transition:opacity .12s;z-index:9;box-shadow:0 3px 14px rgba(0,0,0,.18)}
.toggle{background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--ink2);margin:8px 0}
.sw{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
"""

TIP_JS = """
const tip=document.getElementById('tip');
function showTip(e,html){tip.innerHTML=html;tip.style.opacity=1;
 let x=e.clientX+14,y=e.clientY+12;
 if(x+340>innerWidth)x=e.clientX-345;if(y+120>innerHeight)y=e.clientY-110;
 tip.style.left=x+'px';tip.style.top=y+'px';}
function hideTip(){tip.style.opacity=0}
function tbl(id){const t=document.getElementById(id);t.hidden=!t.hidden}
"""

def page(title, spec, body, extra_css="", extra_js=""):
    return f"""<title>{esc(title)}</title>
<style>{BASE_CSS}{extra_css}</style>
<div class="banner">Attorney Work Product — Privileged &amp; Confidential</div>
<div class="wrap">
<h1>{esc(spec.get('title', title))}</h1>
<p class="sub">{esc(spec.get('subtitle',''))} <span class="num">· updated {esc(spec.get('updated',''))}</span></p>
{body}
</div><div id="tip"></div>
<script>{TIP_JS}{extra_js}</script>"""

def num(v, pick="lo"):
    if isinstance(v, str):
        v = v.replace("$", "").replace(",", "").strip()
        parts = [p for p in v.replace("—","–").replace(" to ","–").replace("-","–").split("–") if p.strip()]
        v = parts[0 if pick == "lo" else -1]
        return float(v)
    return float(v)

def money(n):
    n = num(n)
    if n >= 1_000_000: return f"${n/1_000_000:.4g}M"
    if n >= 1_000: return f"${n/1_000:.4g}K"
    return f"${n:,.0f}"

# ---------------- 1. damages waterfall (ladder, log scale) ----------------
def waterfall():
    spec = json.load(open(f"{WD}/data/viz/damages-waterfall.json"))
    items = spec["data"]
    LO, HI = 10_000, 130_000_000
    def x(v): return (math.log10(max(num(v), LO)) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * 100
    LBL = {"DOCUMENTED":"var(--s3)","DOCUMENTED-PENDING":"var(--s4)","ESTIMABLE":"var(--s1)",
           "MIXED":"var(--s1)","ASSERTED":"var(--s2)","ASSERTED/POSTURE":"var(--crit)","POSTURE":"var(--crit)"}
    def color(lbl):
        for k,v in LBL.items():
            if lbl.upper().startswith(k): return v
        return "var(--s1)"
    rows, cur_tier = [], None
    for it in items:
        if it["tier"] != cur_tier:
            cur_tier = it["tier"]
            rows.append(f'<div class="trow tier"><div class="lbl">TIER {cur_tier}</div><div class="bararea"></div><div class="amt"></div></div>')
        lo, hi = num(it["amount_low"], "lo"), num(it["amount_high"], "hi")
        c = color(it["evidence_label"])
        hatch = "hatch" if ("ASSERT" in it["evidence_label"].upper() or "POSTURE" in it["evidence_label"].upper()) else ""
        dim = "" if it.get("in_totals", True) else "dim"
        total = "total" if it.get("type") == "total" else ""
        left, width = x(lo), max(x(hi) - x(lo), 0.8)
        tip_html = esc(f"<b>{it['label']}</b><br>{money(lo)} – {money(hi)} · {it['evidence_label']}" +
                       (f"<br><i>{it.get('caveat')}</i>" if it.get("caveat") else "") +
                       (f"<br><span class=num>{it.get('trace','')}</span>" if it.get('trace') else "")).replace("&lt;","<").replace("&gt;",">")
        note = "" if it.get("in_totals", True) else ' <span class="chip" style="--c:var(--ink2)">corroboration only — not summed</span>'
        rows.append(f'''<div class="trow {dim} {total}" onmousemove='showTip(event,{json.dumps(tip_html)})' onmouseleave="hideTip()">
<div class="lbl">{esc(it["label"])}{note}</div>
<div class="bararea"><div class="bar {hatch}" style="left:{left:.2f}%;width:{width:.2f}%;--bc:{c}"></div></div>
<div class="amt num">{money(lo)}{"" if lo==hi else " – " + money(hi)}</div></div>''')
    markers = "".join(
        f'''<div class="mline" style="left:{x(m["figure"]):.2f}%" onmousemove='showTip(event,{json.dumps(esc(f"<b>{m['label']}</b><br><i>{m['caveat']}</i>").replace("&lt;","<").replace("&gt;",">"))}' onmouseleave="hideTip()"><span>{money(m["figure"])}</span></div>'''
        for m in spec.get("posture_markers", []))
    axis = "".join(f'<span style="left:{x(v):.2f}%">{money(v)}</span>' for v in [10_000,100_000,1_000_000,10_000_000,100_000_000])
    legend = "".join(f'<span><span class="sw" style="background:{v}"></span>{k}</span>' for k,v in
                     [("DOCUMENTED","var(--s3)"),("DOCUMENTED-PENDING","var(--s4)"),("ESTIMABLE / MIXED","var(--s1)"),("ASSERTED","var(--s2)"),("POSTURE (hatched)","var(--crit)")])
    tbl_rows = "".join(f"<tr><td>{it['tier']}</td><td>{esc(it['label'])}</td><td class='num'>{money(it['amount_low'])}</td><td class='num'>{money(it['amount_high'])}</td><td>{esc(it['evidence_label'])}</td><td>{esc(it.get('caveat') or '')}</td></tr>" for it in items)
    notes = "".join(f"<li>{esc(n)}</li>" for n in spec.get("notes", []))
    body = f"""
<div class="legend">{legend}</div>
<div class="chart card" style="position:relative">
<div class="axis num">{axis}</div>
{"".join(rows)}
<div class="mlayer">{markers}</div>
</div>
<button class="toggle" onclick="tbl('dtable')">table view</button>
<div id="dtable" hidden class="tbox"><table><tr><th>Tier</th><th>Item</th><th>Low</th><th>High</th><th>Label</th><th>Caveat</th></tr>{tbl_rows}</table></div>
<div class="card"><b>Notes</b><ul style="margin:6px 0 0;padding-left:18px;font-size:12px;color:var(--ink2)">{notes}</ul></div>"""
    css = """
.chart{padding:34px 12px 10px}
.axis{position:relative;height:16px;margin:0 260px 6px 300px;border-bottom:1px solid var(--line)}
.axis span{position:absolute;transform:translateX(-50%);font-size:10px;color:var(--ink2)}
.trow{display:flex;align-items:center;gap:8px;padding:2.5px 0}
.trow .lbl{width:292px;font-size:11.5px;text-align:right;flex-shrink:0;color:var(--ink)}
.trow.tier .lbl{font-weight:700;color:var(--navy);letter-spacing:.08em;font-size:11px}
.trow .bararea{flex:1;position:relative;height:15px}
.trow .amt{width:252px;font-size:11px;color:var(--ink2);flex-shrink:0}
.bar{position:absolute;top:2px;height:11px;border-radius:0 4px 4px 0;background:var(--bc);min-width:5px}
.bar.hatch{background:repeating-linear-gradient(45deg,var(--bc),var(--bc) 4px,transparent 4px,transparent 8px);border:1px solid var(--bc)}
.trow.dim{opacity:.55}
.trow.total .lbl{font-weight:600}
.trow:hover .bar{outline:2px solid var(--paper);box-shadow:0 0 0 3px var(--bc)}
.mlayer{position:absolute;inset:34px 264px 10px 304px;pointer-events:none}
.mline{position:absolute;top:0;bottom:0;border-left:2px dashed var(--crit);pointer-events:auto}
.mline span{position:absolute;top:-18px;transform:translateX(-50%);font-size:10.5px;color:var(--crit);font-weight:700;white-space:nowrap}
@media (max-width:760px){.trow .lbl{width:150px}.trow .amt{width:90px}.axis{margin:0 98px 6px 158px}.mlayer{inset:34px 102px 10px 162px}}
"""
    open(f"{V}/damages-waterfall.html","w").write(page("Damages Waterfall", spec, body, css))

# ---------------- 2. case timeline ----------------
def timeline():
    spec = json.load(open(f"{WD}/data/viz/case-timeline.json"))
    pm = json.load(open(f"{WD}/data/viz/pressure-map.json"))
    events = list(spec["data"])
    key_dates = pm.get("key_dates", [])
    cards = []
    for e in events:
        flags = "".join(f'<span class="chip" style="--c:var(--warn)">⚑ {esc(f)}</span> ' for f in e.get("flags", []))
        unres = "unres" if "UNRESOLVED" in str(e.get("year","")).upper() else ""
        cards.append(f'''<div class="ev {unres}">
<div class="dot" style="--c:var(--s1)"></div>
<div class="when num">{esc(e["date"])}<br><span class="yr">{esc(e["year"])}</span></div>
<div class="what"><b>{esc(e["event"])}</b>
<div class="st">{esc(e.get("status",""))}</div>{flags}
<div class="src num">{esc(", ".join(e.get("sources", [])))}</div></div></div>''')
    for k in key_dates:
        cards.append(f'''<div class="ev clockev">
<div class="dot" style="--c:var(--crit)"></div>
<div class="when num">{esc(k["date"])}</div>
<div class="what"><b>⏰ {esc(k["event"])}</b></div></div>''')
    tblr = "".join(f"<tr><td>{esc(e['date'])}</td><td>{esc(e['year'])}</td><td>{esc(e['event'])}</td><td>{esc(e.get('status',''))}</td></tr>" for e in events) + \
           "".join(f"<tr><td>{esc(k['date'])}</td><td></td><td>{esc(k['event'])}</td><td>deadline</td></tr>" for k in key_dates)
    notes = "".join(f"<li>{esc(n)}</li>" for n in spec.get("notes", []))
    body = f"""
<div class="legend"><span><span class="sw" style="background:var(--s1)"></span>case events</span>
<span><span class="sw" style="background:var(--crit)"></span>clocks / deadlines</span>
<span><span class="chip" style="--c:var(--warn)">⚑</span> open factual flag — not yet resolved against documents</span></div>
<div class="tl">{"".join(cards)}</div>
<button class="toggle" onclick="tbl('ttable')">table view</button>
<div id="ttable" hidden class="tbox"><table><tr><th>Date</th><th>Year</th><th>Event</th><th>Status</th></tr>{tblr}</table></div>
<div class="card"><b>Notes</b><ul style="margin:6px 0 0;padding-left:18px;font-size:12px;color:var(--ink2)">{notes}</ul></div>"""
    css = """
.tl{border-left:2px solid var(--line);margin:14px 0 14px 8px;padding-left:0}
.ev{display:flex;gap:12px;padding:9px 0;position:relative}
.dot{width:13px;height:13px;border-radius:50%;background:var(--c);flex-shrink:0;margin-left:-7.5px;margin-top:3px;outline:2px solid var(--paper)}
.ev.unres .dot{background:var(--paper);border:3px dashed var(--c)}
.when{width:120px;flex-shrink:0;font-size:12px;font-weight:700;color:var(--navy)}
.when .yr{font-weight:400;font-size:10.5px;color:var(--ink2)}
.what{flex:1;font-size:13px;max-width:78ch}
.st{color:var(--ink2);font-size:12px;margin:2px 0 4px}
.src{font-size:10.5px;color:var(--ink2)}
.clockev .what b{color:var(--crit)}
"""
    open(f"{V}/case-timeline.html","w").write(page("Case Timeline", spec, body, css))

# ---------------- 3. pressure map ----------------
def pressure():
    spec = json.load(open(f"{WD}/data/viz/pressure-map.json"))
    nodes, edges = spec["data"], spec["edges"]
    W, H, CX, CY = 900, 620, 450, 300
    pos = {}
    ring = [n for n in nodes if n["id"] != "plaintiff"]
    center = next((n for n in nodes if n["id"] == "plaintiff"), None)
    if center: pos["plaintiff"] = (CX, CY)
    for i, n in enumerate(ring):
        a = -math.pi/2 + i * 2*math.pi/len(ring)
        pos[n["id"]] = (CX + 300*math.cos(a), CY + 225*math.sin(a))
    svg_edges = []
    for e in edges:
        if e["from"] not in pos or e["to"] not in pos: continue
        x1,y1 = pos[e["from"]]; x2,y2 = pos[e["to"]]
        ks = e.get("keystone")
        tip_e = esc(f"<b>{e['instrument']}</b> · {e['from']} → {e['to']}<br>{e['what_it_exposes']}" + ("<br><b>KEYSTONE evidence path</b>" if ks else "")).replace("&lt;","<").replace("&gt;",">")
        svg_edges.append(f'''<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"
 stroke="{'var(--maroon)' if ks else 'var(--line)'}" stroke-width="{3 if ks else 1.6}" {'stroke-dasharray="none"' if ks else ''}
 onmousemove='showTip(event,{json.dumps(tip_e)})' onmouseleave="hideTip()" style="cursor:pointer"/>''')
    svg_nodes = []
    for n in nodes:
        x, y = pos[n["id"]]
        r = 14 + n["exposure_rating"] * 5
        is_p = n["id"] == "plaintiff"
        fill = "var(--s3)" if is_p else ("var(--s1)" if "defendant" in n["role"].lower() else "var(--s7)")
        tip_n = esc(f"<b>{n['name']}</b><br>{n['role']}<br>Exposure: {n['exposure_rating']}/5<br><b>Fears:</b> {n['top_fear']}<br><b>Contradiction:</b> {n['key_contradiction']}").replace("&lt;","<").replace("&gt;",">")
        short = n["name"].split(",")[0].split("(")[0].strip()
        if len(short) > 22: short = short[:20] + "…"
        svg_nodes.append(f'''<g onmousemove='showTip(event,{json.dumps(tip_n)})' onmouseleave="hideTip()" style="cursor:pointer">
<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" opacity="0.88" stroke="var(--paper)" stroke-width="2"/>
<text x="{x:.0f}" y="{y + r + 14:.0f}" text-anchor="middle" font-size="11.5" fill="var(--ink)" font-weight="600">{esc(short)}</text>
<text x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700" class="num">{n['exposure_rating']}</text></g>''')
    ntbl = "".join(f"<tr><td>{esc(n['name'])}</td><td>{n['exposure_rating']}/5</td><td>{esc(n['top_fear'])}</td><td>{esc(n['key_contradiction'])}</td></tr>" for n in nodes)
    etbl = "".join(f"<tr><td>{esc(e['from'])} → {esc(e['to'])}</td><td>{esc(e['instrument'])}</td><td>{esc(e['what_it_exposes'])}</td><td>{'⭐' if e.get('keystone') else ''}</td></tr>" for e in edges)
    notes = "".join(f"<li>{esc(n)}</li>" for n in spec.get("notes", []))
    body = f"""
<div class="legend"><span><span class="sw" style="background:var(--s1)"></span>defendant</span>
<span><span class="sw" style="background:var(--s7)"></span>non-party</span>
<span><span class="sw" style="background:var(--s3)"></span>plaintiff</span>
<span><span class="sw" style="background:var(--maroon)"></span>keystone evidence path (thick)</span>
<span>node size &amp; number = exposure rating /5 · hover everything</span></div>
<div class="card" style="padding:4px"><svg viewBox="0 0 {W} {H}" style="width:100%;height:auto">{"".join(svg_edges)}{"".join(svg_nodes)}</svg></div>
<button class="toggle" onclick="tbl('ptable')">table view</button>
<div id="ptable" hidden class="tbox">
<table><tr><th>Party</th><th>Exposure</th><th>Top fear</th><th>Key contradiction</th></tr>{ntbl}</table>
<table><tr><th>Leverage line</th><th>Instrument</th><th>What it exposes</th><th>Keystone</th></tr>{etbl}</table></div>
<div class="card"><b>Notes</b><ul style="margin:6px 0 0;padding-left:18px;font-size:12px;color:var(--ink2)">{notes}</ul></div>"""
    open(f"{V}/pressure-map.html","w").write(page("Pressure-Point Map", spec, body))

# ---------------- 4. action tracker ----------------
def tracker():
    spec = json.load(open(f"{WD}/data/viz/action-tracker.json"))
    items = spec["data"]
    def urgency(it):
        if "completed" in it["status"]: return ("done","var(--good)","✓ done")
        txt = (str(it.get("deadline","")) + it.get("schedule_note","") + it["item"]).lower()
        wk = str(it.get("week",""))
        if "sol" in txt or "sept" in txt or "statute" in txt or wk in ("W1","W2"): return ("crit","var(--crit)","SoL-critical")
        if wk in ("W3","W4","W5","W6"): return ("high","var(--warn)","high")
        return ("norm","var(--s1)","normal")
    def owner_short(o):
        o = o.lower()
        if "shared" in o: return "Shared"
        if "faraaz" in o: return "Faraaz"
        if "drazen" in o or "douglas" in o: return "Drazen"
        if "haseeb" in o: return "Haseeb"
        return "Family"
    owners = sorted({owner_short(i["owner"]) for i in items})
    rows = []
    for it in sorted(items, key=lambda i: (str(i.get("week","W99")), i["id"])):
        u, uc, ul = urgency(it)
        ow = owner_short(it["owner"])
        tip_i = esc(f"<b>{it['id']}</b> {it['item']}<br><b>Owner:</b> {it['owner']}<br><b>Deadline:</b> {it.get('deadline','—')}<br><i>{it.get('schedule_note','')}</i>").replace("&lt;","<").replace("&gt;",">")
        rows.append(f'''<div class="item" data-o="{ow}" data-u="{u}" data-t="{esc((it['id']+it['item']).lower())}"
 onmousemove='showTip(event,{json.dumps(tip_i)})' onmouseleave="hideTip()">
<span class="wk num">{esc(it.get("week","—"))}</span>
<span class="chip" style="--c:{uc}">{ul}</span>
<span class="chip" style="--c:var(--navy)">{ow}</span>
<span class="id num">{esc(it["id"])}</span>
<span class="txt">{esc(it["item"][:150])}{"…" if len(it["item"])>150 else ""}</span></div>''')
    chips = "".join(f'<button class="fchip" data-f="{o}">{o}</button>' for o in owners)
    tblr = "".join(f"<tr><td class='num'>{esc(i['id'])}</td><td>{esc(i.get('week',''))}</td><td>{esc(i['owner'])}</td><td>{esc(i['item'])}</td><td>{esc(i.get('deadline',''))}</td><td>{esc(i['status'])}</td></tr>" for i in items)
    body = f"""
<div class="legend"><span class="chip" style="--c:var(--crit)">SoL-critical</span>
<span class="chip" style="--c:var(--warn)">high (W3–W6)</span>
<span class="chip" style="--c:var(--s1)">normal</span>
<span class="chip" style="--c:var(--good)">✓ done</span>
<span style="margin-left:auto">pacing: ≤2 substantive Faraaz tasks/week · retrieval batched</span></div>
<div class="controls">{chips}<input id="q" type="search" placeholder="search…"><span id="n" class="sub"></span></div>
<div id="list">{"".join(rows)}</div>
<button class="toggle" onclick="tbl('atable')">table view</button>
<div id="atable" hidden class="tbox"><table><tr><th>ID</th><th>Week</th><th>Owner</th><th>Item</th><th>Deadline</th><th>Status</th></tr>{tblr}</table></div>"""
    css = """
.controls{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:10px 0}
.fchip{border:1px solid var(--navy);color:var(--navy);background:transparent;border-radius:14px;padding:2px 12px;font-size:12px;cursor:pointer}
.fchip.on{background:var(--navy);color:var(--paper)}
#q{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:5px 9px;font-size:13px;min-width:150px}
.item{display:flex;gap:9px;align-items:baseline;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:7px 11px;margin:5px 0;font-size:13px}
.item .wk{width:78px;font-size:11px;font-weight:700;color:var(--navy);flex-shrink:0}
.item .id{color:var(--ink2);font-size:11px;flex-shrink:0}
.item .txt{flex:1;min-width:220px}
.hidden{display:none}
"""
    js = """
const items=[...document.querySelectorAll('.item')],fchips=[...document.querySelectorAll('.fchip')],
q=document.getElementById('q'),n=document.getElementById('n');let act=new Set();
function ap(){const s=q.value.toLowerCase();let v=0;
 items.forEach(i=>{let ok=(!act.size||act.has(i.dataset.o));if(s&&!i.dataset.t.includes(s))ok=false;
 i.classList.toggle('hidden',!ok);if(ok)v++});n.textContent=v+' / '+items.length;}
fchips.forEach(c=>c.onclick=()=>{c.classList.toggle('on');const f=c.dataset.f;act.has(f)?act.delete(f):act.add(f);ap()});
q.oninput=ap;ap();
"""
    open(f"{V}/action-tracker.html","w").write(page("Action Tracker", spec, body, css, js))

waterfall(); timeline(); pressure(); tracker()
import re
for f in sorted(os.listdir(V)):
    t = open(f"{V}/{f}").read()
    ext = len(re.findall(r'(?:src|href)=["\']https?://', t))
    print(f"OK {f} ({len(t)//1024}KB, external refs: {ext})")
