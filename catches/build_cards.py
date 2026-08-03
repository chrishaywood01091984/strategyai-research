"""StrategyAI catch cards, 1200x1400 (LinkedIn portrait-landscape hybrid).

Top half: the proof. Headline, dials, method, timeline, lead-time badge.
Bottom half: the intelligence. Who it is for, what we told partners, what to do,
and who to approach with names and emails blurred.

Every event traces to a signal we hold. Sources are described by category, never named.
Contact names and emails are blurred by design: roles are the proof, names are the product.

Render: python build_cards.py  then the Edge headless screenshot at 1200x1400.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

TPL = """<title>StrategyAI · {title_tag}</title>
<style>
  :root{{--navy:#0d1b2a;--gold:#c9a84c;--gold-dim:#7d6a31;--ink:#eef3f8;--muted:#8ba0b6}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:#050b12;display:flex;justify-content:center;
    font-family:"Libre Baskerville",Georgia,serif}}
  .card{{position:relative;width:1200px;height:1140px;flex:0 0 auto;color:var(--ink);
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

  .method{{position:absolute;left:812px;top:240px;width:344px;padding:10px 14px 11px;
    border:1px solid rgba(201,168,76,.3);border-left:3px solid var(--gold);border-radius:3px;
    background:rgba(201,168,76,.06)}}
  .method h4{{margin:0 0 5px;font-family:"DM Mono",monospace;font-size:8.5px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--gold);font-weight:400}}
  .method .row{{font-family:"DM Mono",monospace;font-size:8.6px;letter-spacing:.06em;
    text-transform:uppercase;color:#cfdcea;line-height:1.7}}
  .method p{{margin:5px 0 0;font-size:10.5px;line-height:1.4;color:var(--muted)}}
  .method p b{{color:#fff;font-weight:700}}

  .spine{{position:absolute;left:44px;right:44px;top:372px;height:2px;
    background:linear-gradient(90deg,rgba(201,168,76,.22),rgba(201,168,76,.5))}}
  .run{{position:absolute;top:370px;height:6px;border-radius:3px;
    background:linear-gradient(90deg,var(--gold),#e6cd86)}}
  .pill{{position:absolute;top:342px;transform:translateX(-50%);white-space:nowrap;
    display:flex;align-items:center;gap:11px;padding:9px 22px 9px 20px;border-radius:7px;
    background:linear-gradient(135deg,#f0dc9d 0%,#c9a84c 55%,#b0902f 100%);color:#0d1b2a;
    box-shadow:0 0 0 7px rgba(13,27,42,.96),0 8px 26px rgba(201,168,76,.42)}}
  .pill .num{{font-family:"Playfair Display",Georgia,serif;font-size:40px;line-height:.9;
    font-weight:700;letter-spacing:-.01em}}
  .pill .txt{{font-family:"DM Mono",monospace;font-size:11.5px;line-height:1.28;
    letter-spacing:.19em;text-transform:uppercase;font-weight:700;text-align:left}}

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

  /* ---------- lower half: the intelligence ---------- */
  .split{{position:absolute;left:44px;right:44px;top:600px;height:1px;
    background:linear-gradient(90deg,var(--gold),rgba(201,168,76,.1))}}
  .banner{{position:absolute;left:44px;top:624px;font-family:"DM Mono",monospace;font-size:10px;
    letter-spacing:.26em;text-transform:uppercase;color:var(--gold)}}
  .banner span{{color:var(--muted);letter-spacing:.16em}}

  .cols{{position:absolute;left:44px;right:44px;top:660px;display:flex;gap:26px}}
  .col{{flex:1;border-top:2px solid rgba(201,168,76,.35);padding-top:14px}}
  .col h5{{margin:0 0 9px;font-family:"DM Mono",monospace;font-size:9px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--gold);font-weight:400}}
  .col .who{{font-size:13px;line-height:1.5;color:#fff;font-weight:700}}
  .col .whosub{{font-family:"DM Mono",monospace;font-size:9px;letter-spacing:.09em;
    text-transform:uppercase;color:var(--muted);margin-top:7px;line-height:1.7}}
  .col p{{margin:0;font-size:12.5px;line-height:1.62;color:#cfdcea}}
  .col .stamp{{font-family:"DM Mono",monospace;font-size:8.5px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--muted);margin-bottom:7px}}

  .approach{{position:absolute;left:44px;right:44px;top:845px;border:1px solid rgba(201,168,76,.28);
    border-radius:6px;background:rgba(201,168,76,.05);padding:18px 22px 20px}}
  .approach h5{{margin:0 0 3px;font-family:"DM Mono",monospace;font-size:10px;letter-spacing:.22em;
    text-transform:uppercase;color:var(--gold);font-weight:400}}
  .approach .lead{{font-size:12px;color:var(--muted);margin:0 0 15px;line-height:1.5}}
  .people{{display:flex;gap:16px}}
  .person{{flex:1;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);
    border-radius:5px;padding:12px 14px}}
  .redact{{height:13px;border-radius:2px;background:linear-gradient(90deg,#93a7bb,#6f8398);
    filter:blur(3.6px);opacity:.85;margin-bottom:7px}}
  .redact.e{{height:10px;width:88%;background:linear-gradient(90deg,#7f93a8,#5d7189);
    margin-bottom:11px}}
  .person .role{{font-size:12px;line-height:1.45;color:#fff;font-weight:700}}
  .person .org{{font-family:"DM Mono",monospace;font-size:8.5px;letter-spacing:.1em;
    text-transform:uppercase;color:var(--gold);margin-top:5px}}

  footer{{position:absolute;left:44px;right:44px;bottom:26px;display:flex;
    justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.09);
    padding-top:14px;font-family:"DM Mono",monospace;font-size:9.5px;letter-spacing:.15em;
    text-transform:uppercase;color:var(--muted)}}
  .wm{{font-family:"Playfair Display",serif;font-size:15px;letter-spacing:.02em;color:#fff;
    text-transform:none}}
  .wm b{{color:var(--gold);font-weight:600}}
  .basis{{position:absolute;left:44px;right:44px;bottom:74px;text-align:center;
    font-family:"DM Mono",monospace;font-size:9px;letter-spacing:.16em;text-transform:uppercase;
    color:#6f8298}}
</style>
<div class="card">
  <div class="eyebrow">Before the mandate · Proof</div>
  <h1>{headline}</h1>
  <p class="sub">{sub}</p>
  <div class="dials">{dials}</div>
  <div class="method">
    <h4>How the signal is built</h4>
    <div class="row">Behavioural patterns · Hiring trends · Velocity<br>Sequenced into one situation</div>
    <p><b>The evidence</b>, <b>who to approach</b>, <b>why now</b>.</p>
  </div>
  <div class="spine"></div>
  <div class="run" style="left:{run_from}px;width:{run_w}px"></div>
  <div class="pill" style="left:{pill_x}px"><span class="num">{pill_num}</span><span class="txt">{pill_txt}</span></div>
  {events}

  <div class="split"></div>
  <div class="banner">What our partners received <span>· on the day we surfaced it</span></div>
  <div class="cols">
    <div class="col">
      <h5>Who this is for</h5>
      <div class="who">{for_who}</div>
      <div class="whosub">{for_work}</div>
    </div>
    <div class="col">
      <h5>What we told them</h5>
      <div class="stamp">{told_date}</div>
      <p>{told}</p>
    </div>
    <div class="col">
      <h5>What we said to do</h5>
      <div class="stamp">The next move</div>
      <p>{todo}</p>
    </div>
  </div>

  <div class="approach">
    <h5>Who to approach</h5>
    <p class="lead">Named individuals and direct email addresses were supplied to partners. Redacted here.</p>
    <div class="people">{people}</div>
  </div>

  <div class="basis">Behaviour patterns mapped across 15,000+ awarded mandates and 55,000 tracked signals</div>
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

PERSON = """<div class="person">
  <div class="redact"></div><div class="redact e"></div>
  <div class="role">{role}</div><div class="org">{org}</div>
</div>"""


def build(spec):
    dials = "".join(DIAL.format(**d) for d in spec["dials"])
    people = "".join(PERSON.format(**p) for p in spec["people"])
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
            sc = "var(--gold)" if kind == "flag" else (
                "rgba(255,255,255,.45)" if kind == "deal" else "rgba(201,168,76,.3)")
            parts.append(f'<div class="stem" style="left:{x}px;top:388px;height:32px;background:{sc}"></div>')
            top = e.get("top", 420)
        style = f"left:{e.get('lx', x)}px;top:{top}px"
        if e.get("width"):
            style += f";width:{e['width']}px"
        if e.get("align"):
            style += f";text-align:{e['align']}"
        srcstyle = "color:var(--gold)" if kind == "flag" else ""
        parts.append(
            f'<div class="lbl{" hero" if hero else ""}" style="{style}">'
            f'<div class="d">{e["date"]}</div><div class="t">{e["text"]}</div>'
            f'<div class="s" style="{srcstyle}">{e["src"]}</div></div>')
    return TPL.format(events="\n  ".join(parts), dials=dials, people=people, **spec["meta"])


if __name__ == "__main__":
    with open(os.path.join(HERE, "cards.json"), encoding="utf-8") as fh:
        for name, spec in json.load(fh).items():
            with open(os.path.join(HERE, f"{name}.html"), "w", encoding="utf-8") as f:
                f.write(build(spec))
            print("wrote", name + ".html")
