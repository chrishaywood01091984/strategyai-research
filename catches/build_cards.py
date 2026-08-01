"""Generate StrategyAI catch cards (1200x628 LinkedIn landscape) from a data spec.

Every event on a card must trace to a signal we actually hold. Sources are described
by category, never by name, so the method is visible but the feed is not.
Render:  python build_cards.py   then the Edge command in render.txt
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))

# Fixed vertical bands so nothing can collide: h1 54-160, sub 170-236,
# above-labels 244-318, stems 334-372, spine 372, below-labels 420-560.
TPL = """<title>StrategyAI · {title_tag}</title>
<style>
  :root{{--navy:#0d1b2a;--gold:#c9a84c;--gold-dim:#7d6a31;--ink:#eef3f8;--muted:#8ba0b6}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:#050b12;display:flex;justify-content:center;
    font-family:"Libre Baskerville",Georgia,serif}}
  .card{{position:relative;width:1200px;height:628px;flex:0 0 auto;color:var(--ink);
    background:radial-gradient(900px 420px at 12% -14%,#17304a 0%,transparent 62%),var(--navy);
    overflow:hidden}}
  .eyebrow{{position:absolute;left:44px;top:34px;font-family:"DM Mono",ui-monospace,monospace;
    font-size:10px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold)}}
  h1{{position:absolute;left:44px;top:54px;width:630px;height:106px;margin:0;
    font-family:"Playfair Display",Georgia,serif;font-weight:600;font-size:31px;
    line-height:1.14;color:#fff}}
  h1 em{{font-style:normal;color:var(--gold)}}
  .sub{{position:absolute;left:44px;top:170px;width:648px;height:66px;margin:0;
    font-size:12.5px;line-height:1.55;color:var(--muted)}}
  .sub b{{color:#dbe6f1;font-weight:700}}
  .dials{{position:absolute;right:44px;top:44px;display:flex;gap:16px}}
  .dial{{width:104px;text-align:center}}
  .dial p{{font-family:"DM Mono",monospace;font-size:8.5px;letter-spacing:.12em;
    text-transform:uppercase;color:var(--muted);margin:6px 0 0;line-height:1.5}}
  .v{{font-family:"Playfair Display",serif;font-size:24px;fill:#fff}}
  .u{{font-family:"DM Mono",monospace;font-size:7.5px;fill:var(--muted);letter-spacing:.14em}}
  .spine{{position:absolute;left:44px;right:44px;top:372px;height:2px;
    background:linear-gradient(90deg,rgba(201,168,76,.22),rgba(201,168,76,.5))}}
  .run{{position:absolute;top:370px;height:6px;border-radius:3px;
    background:linear-gradient(90deg,var(--gold),#e6cd86)}}
  .pill{{position:absolute;top:359px;transform:translateX(-50%);white-space:nowrap;
    font-family:"DM Mono",monospace;font-size:11px;letter-spacing:.2em;text-transform:uppercase;
    color:var(--navy);background:var(--gold);padding:5px 14px;border-radius:3px;
    box-shadow:0 0 0 5px rgba(13,27,42,.95)}}
  .n{{position:absolute;border-radius:50%;background:var(--navy);border:2px solid var(--gold-dim);
    width:11px;height:11px;top:367px;transform:translateX(-50%)}}
  .n.flag{{width:22px;height:22px;top:362px;background:var(--gold);border:3px solid var(--gold);
    box-shadow:0 0 0 6px rgba(201,168,76,.15)}}
  .n.deal{{width:24px;height:24px;top:361px;background:#fff;border:3px solid #fff;
    box-shadow:0 0 0 6px rgba(255,255,255,.12)}}
  .stem{{position:absolute;width:1px;background:rgba(201,168,76,.3);transform:translateX(-50%)}}
  .lbl{{position:absolute;width:150px;transform:translateX(-50%)}}
  .lbl .d{{font-family:"DM Mono",monospace;font-size:9.5px;letter-spacing:.11em;color:var(--gold)}}
  .lbl .t{{font-size:11.5px;line-height:1.4;color:#cfdcea;margin-top:3px}}
  .lbl .s{{font-family:"DM Mono",monospace;font-size:7.5px;letter-spacing:.09em;
    text-transform:uppercase;color:#6f8298;margin-top:4px}}
  .lbl.hero{{width:200px}}
  .lbl.hero .t{{font-size:13px;color:#fff;font-weight:600;line-height:1.38}}
  .lbl.hero .d{{color:#fff}}
  /* Method panel: sits in the clear zone right of the last above-label, under the dials.
     Describes what we do, not what fired on this deal. */
  .method{{position:absolute;left:812px;top:243px;width:344px;padding:11px 14px 12px;
    border:1px solid rgba(201,168,76,.3);border-left:3px solid var(--gold);border-radius:3px;
    background:rgba(201,168,76,.06)}}
  .method h4{{margin:0 0 6px;font-family:"DM Mono",monospace;font-size:8.5px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--gold);font-weight:400}}
  .method .row{{font-family:"DM Mono",monospace;font-size:9px;letter-spacing:.07em;
    text-transform:uppercase;color:#cfdcea;line-height:1.85}}
  .method p{{margin:6px 0 0;font-size:10.5px;line-height:1.45;color:var(--muted)}}
  .method p b{{color:#fff;font-weight:700}}
  footer{{position:absolute;left:44px;right:44px;bottom:26px;display:flex;
    justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.09);
    padding-top:14px;font-family:"DM Mono",monospace;font-size:9.5px;letter-spacing:.15em;
    text-transform:uppercase;color:var(--muted)}}
  .wm{{font-family:"Playfair Display",serif;font-size:15px;letter-spacing:.02em;color:#fff;
    text-transform:none}}
  .wm b{{color:var(--gold);font-weight:600}}
</style>
<div class="card">
  <div class="eyebrow">Before the mandate · Proof</div>
  <h1>{headline}</h1>
  <p class="sub">{sub}</p>
  <div class="dials">{dials}</div>
  <div class="method">
    <h4>How the signal is built</h4>
    <div class="row">Behavioural patterns · Hiring trends<br>Signal velocity · Sequenced as one situation</div>
    <p>Partners get <b>the evidence</b>, <b>who to approach</b>, and <b>why the timing works now</b>.</p>
  </div>
  <div class="spine"></div>
  <div class="run" style="left:{run_from}px;width:{run_w}px"></div>
  <div class="pill" style="left:{pill_x}px">{pill}</div>
  {events}
  <footer>
    <div class="wm">Strategy<b>AI</b></div>
    <div>{strap}</div>
    <div>strategyai.co.uk</div>
  </footer>
</div>
"""

DIAL = """<div class="dial"><svg width="104" height="104" viewBox="0 0 104 104">
  <circle cx="52" cy="52" r="42" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="8"/>
  <circle cx="52" cy="52" r="42" fill="none" stroke="{colour}" stroke-width="8"
    stroke-linecap="round" stroke-dasharray="{dash} 264" transform="rotate(-90 52 52)"/>
  <text class="v" x="52" y="50" text-anchor="middle">{value}</text>
  <text class="u" x="52" y="65" text-anchor="middle">{unit}</text>
</svg><p>{caption}</p></div>"""


def build(spec):
    dials = "".join(DIAL.format(**d) for d in spec["dials"])
    parts = []
    for e in spec["events"]:
        x, kind = e["x"], e.get("kind", "")
        cls = {"flag": "n flag", "deal": "n deal"}.get(kind, "n")
        hero = kind in ("flag", "deal")
        parts.append(f'<div class="{cls}" style="left:{x}px"></div>')
        if e["side"] == "above":
            parts.append(f'<div class="stem" style="left:{x}px;top:334px;height:38px"></div>')
            top = e.get("top", 252)
        else:
            stem_c = "var(--gold)" if kind == "flag" else (
                "rgba(255,255,255,.45)" if kind == "deal" else "rgba(201,168,76,.3)")
            parts.append(f'<div class="stem" style="left:{x}px;top:388px;height:32px;'
                         f'background:{stem_c}"></div>')
            top = e.get("top", 420)
        style = f"left:{e.get('lx', x)}px;top:{top}px"
        if e.get("width"):
            style += f";width:{e['width']}px"
        if e.get("align"):
            style += f";text-align:{e['align']}"
        sc = ';color:var(--gold)' if kind == "flag" else ''
        parts.append(
            f'<div class="lbl{" hero" if hero else ""}" style="{style}">'
            f'<div class="d">{e["date"]}</div><div class="t">{e["text"]}</div>'
            f'<div class="s" style="{sc.lstrip(";")}">{e["src"]}</div></div>')
    return TPL.format(events="\n  ".join(parts), dials=dials, **spec["meta"])


if __name__ == "__main__":
    with open(os.path.join(HERE, "cards.json"), encoding="utf-8") as fh:
        for name, spec in json.load(fh).items():
            out = os.path.join(HERE, f"{name}.html")
            with open(out, "w", encoding="utf-8") as f:
                f.write(build(spec))
            print("wrote", os.path.basename(out))
