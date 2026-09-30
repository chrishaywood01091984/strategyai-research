"""Proof-it-works cards in the hero signal card's visual language.

White card, gradient header band and edge, Gloock + Hanken Grotesk, dark blue
with colour-coded evidence (violet flag, blue bids, green deals, slate press,
terracotta filings), a "days ahead" ring, tinted panels. 1200x1600, rendered
at 2x with Edge headless to <name>-proof.png.

usage: python build_proof.py
"""
import os, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "proof"); os.makedirs(OUT, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

INK = {"FLAGGED": "#7A4FA0", "BID": "#3E6491", "DEAL": "#1D9E75", "PRESS": "#5E7389",
       "FILING": "#C0643F", "COMPANY": "#2F84B0", "VOTE": "#3E6491"}
BAR = ["#7A4FA0", "#3E6491", "#1D9E75", "#5B84A8"]
FLAG = {
    "GB": '<svg viewBox="0 0 60 30"><clipPath id="c"><path d="M0,0 v30 h60 v-30 z"/></clipPath><clipPath id="t"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath><g clip-path="url(#c)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#t)" stroke="#C8102E" stroke-width="4"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
    "DE": '<svg viewBox="0 0 3 2"><rect width="3" height="2" fill="#FFCE00"/><rect width="3" height="1.333" fill="#DD0000"/><rect width="3" height=".667" fill="#000"/></svg>',
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:1600px;background:#fff;font-family:'Hanken Grotesk',system-ui,sans-serif;color:#0F1B2D;
  font-synthesis:none;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased;overflow:hidden}
.card{position:relative;width:1200px;height:1600px;background:#fff;overflow:hidden;display:flex;flex-direction:column}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:10px;background:linear-gradient(#7A4FA0,#3E6491 45%,#1D9E75);z-index:2}
.ml{font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase}
.hd{display:flex;align-items:center;gap:14px;padding:18px 44px 18px 52px;background:linear-gradient(90deg,#0F2A44,#1F5F86)}
.hd .flag{width:34px;height:23px;border-radius:3px;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,.35);flex:none}
.hd .flag svg{display:block;width:100%;height:100%}
.hd .dot{width:10px;height:10px;border-radius:50%;background:#3CCB95;flex:none}
.hd .t{color:#8FE3C0;margin-right:auto}
.hd .strap{color:#C9D7E6;font-weight:600}
.hd .chip{background:#D9483B;color:#fff;border-radius:5px;padding:6px 12px;font-size:13px;letter-spacing:.14em}
.bd{flex:1;display:flex;flex-direction:column;justify-content:space-evenly;gap:18px;padding:24px 44px 12px 52px}
.top{display:grid;grid-template-columns:1fr 176px;gap:28px;align-items:start}
.co{font-family:'Gloock',Georgia,serif;font-size:58px;line-height:1.02;letter-spacing:-.01em}
.loc{color:#1F5F86;margin-top:8px}
.pair{display:flex;align-items:center;gap:12px;margin-top:14px;flex-wrap:wrap}
.mark{height:40px;min-width:92px;padding:6px 14px;border:1px solid #D8DFE6;border-radius:6px;background:#F6F8FA;display:flex;align-items:center;justify-content:center;
  font-family:'Gloock',Georgia,serif;font-size:18px;letter-spacing:.03em;color:#0F1B2D}
.mark img{max-height:24px;max-width:120px}
.arrow{color:#3E6491;font-size:22px}
.deal{display:inline-block;background:linear-gradient(135deg,#1F5F86,#1D9E75);color:#fff;border-radius:5px;padding:9px 14px;font-size:14px}
.deal b{font-family:'Gloock',Georgia,serif;font-weight:400;font-size:20px;letter-spacing:0;margin-left:8px;text-transform:none}
.ring{position:relative;width:176px;height:176px}
.ring svg{width:176px;height:176px;transform:rotate(-90deg)}
.ring .n{position:absolute;inset:0;display:grid;place-items:center;text-align:center}
.ring .n b{display:block;font-weight:700;font-size:58px;line-height:1;color:#1F5F86}
.ring .n span{display:block;font-weight:700;font-size:12px;letter-spacing:.12em;color:#5B6878;margin-top:6px;text-transform:uppercase}
h1{font-family:'Gloock',Georgia,serif;font-weight:400;font-size:37px;line-height:1.14;letter-spacing:-.005em;text-wrap:balance}
h1 em{font-style:normal;color:#3E6491}
.stand{font-size:17px;line-height:1.6;color:#3D4A5C;margin-top:10px}
.stand b{color:#0F1B2D;font-weight:600}
.meta{display:flex;align-items:center;gap:8px;font-size:14px;color:#5B6878;margin-top:10px}
.meta::before{content:"";width:9px;height:9px;border-radius:50%;background:#1D9E75}
.sqh{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.sqh .l{color:#3E6491}.sqh .r{color:#14795A}
.seq{position:relative;list-style:none;display:grid;gap:12px;padding-left:34px}
.seq::before{content:"";position:absolute;left:10px;top:10px;bottom:10px;width:2px;background:linear-gradient(#7A4FA0,#3E6491,#1D9E75)}
.seq li{position:relative;display:grid;grid-template-columns:92px 1fr auto;gap:16px;align-items:baseline}
.seq li::before{content:"";position:absolute;left:-31px;top:4px;width:14px;height:14px;border-radius:50%;background:var(--c);box-shadow:0 0 0 4px color-mix(in srgb,var(--c) 18%,#fff)}
.seq time{font-weight:600;font-size:16px;color:var(--c)}
.seq .ev{font-size:17px;line-height:1.4}
.tag{display:inline-block;background:var(--c);color:#fff;font-weight:700;font-size:11.5px;letter-spacing:.1em;border-radius:4px;padding:3px 8px;margin-right:10px;vertical-align:2px}
.seq .dd{font-weight:700;font-size:13px;letter-spacing:.08em;color:var(--c);white-space:nowrap}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.pn{border-radius:10px;padding:18px 20px 16px}
.pn.a{background:linear-gradient(135deg,#EEF1FB,#EAF6F1);border:1px solid #D9E2F0;border-left:4px solid #7A4FA0}
.pn.b{background:linear-gradient(135deg,#EDF4FA,#F2F5FB);border:1px solid #D6E3EE;border-left:4px solid #3E6491}
.pn .ml{margin-bottom:12px}.pn.a .ml{color:#7A4FA0}.pn.b .ml{color:#3E6491}
.bars{display:grid;gap:10px}
.br{display:grid;grid-template-columns:132px 1fr;gap:10px;align-items:center}
.br .k{font-weight:600;font-size:12.5px;letter-spacing:.06em;color:#3D4A5C;text-transform:uppercase;white-space:nowrap}
.br .tr{position:relative;height:22px;background:#DCE3EE;border-radius:4px}
.br .tr i{position:absolute;top:0;bottom:0;border-radius:4px}
.br .tr em{position:absolute;top:1px;font-style:normal;font-weight:700;font-size:13.5px;white-space:nowrap}
.br .st{position:absolute;right:-2px;top:-17px;font-weight:700;font-size:10.5px;letter-spacing:.1em}
.note{font-size:13.5px;line-height:1.5;color:#5B6878;margin-top:12px}
.chk{display:grid;gap:9px}
.chk div{display:grid;grid-template-columns:24px 1fr;gap:8px;font-size:15px;line-height:1.35}
.chk b{font-weight:700;font-size:16px}.chk small{display:block;color:#5B6878;font-size:13px}
.hold{display:grid;gap:12px}
.hold div{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;border-bottom:1px solid #D9E2F0;padding-bottom:10px}
.hold div:last-child{border-bottom:0;padding-bottom:0}
.hold .nm{font-family:'Gloock',Georgia,serif;font-size:22px}.hold small{display:block;color:#5B6878;font-size:13px;margin-top:2px}
.pill{font-weight:700;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;border-radius:4px;padding:4px 9px;color:#fff;white-space:nowrap}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kp{border:1px solid #E2E8EE;border-radius:9px;padding:12px 14px;background:#F8FAFC}
.kp .ml{font-size:11px;color:#5B6878}.kp b{display:block;font-family:'Gloock',Georgia,serif;font-weight:400;font-size:19px;line-height:1.2;margin-top:6px;color:#0F2A44}
.route{background:#EFF8F4;border:1px solid #D3EBDF;border-radius:10px;padding:16px 20px 18px}
.route .h{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.route .h .ml{color:#14795A}.route .h span{font-size:13px;color:#5B6878}
.ppl{display:grid;gap:12px}
.pp{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:center;background:#fff;border:1px solid #D3EBDF;border-radius:8px;padding:12px}
.av{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#7A4FA0,#3E6491);filter:blur(1.5px)}
.pp .rd{height:10px;width:62%;border-radius:3px;background:linear-gradient(90deg,#9FB0C2,#C9D3DE);filter:blur(3px);margin-bottom:8px}
.pp b{display:block;font-weight:700;font-size:15px}.pp small{display:block;font-size:12.5px;color:#5B6878;margin-top:2px}
.deg{display:inline-block;margin-top:6px;font-weight:700;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#14795A;border:1px solid #9FD3BC;border-radius:3px;padding:2px 7px}
.hs{background:linear-gradient(135deg,#EEF1FB,#EAF6F1);border:1px solid #D9E2F0;border-left:4px solid #7A4FA0;border-radius:10px;padding:18px 22px 20px}
.hs .top2{display:flex;justify-content:space-between;align-items:baseline;gap:16px}
.hs .ml{color:#7A4FA0}.hs .big{font-family:'Gloock',Georgia,serif;font-size:27px;line-height:1.2;color:#0F2A44;margin-top:6px}
.hs .big em{font-style:normal;color:#1D9E75}
.hs .days{font-weight:700;font-size:15px;color:#0F1B2D;white-space:nowrap}
.trk{position:relative;height:14px;background:#DCE3EE;border-radius:7px;margin:44px 0 40px}
.trk .fill{position:absolute;left:0;top:0;bottom:0;border-radius:7px;background:linear-gradient(90deg,#7A4FA0,#3E6491,#1D9E75)}
.trk .pt{position:absolute;top:50%;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;background:var(--c);border:3px solid #fff;box-shadow:0 0 0 1px var(--c)}
.trk .lb{position:absolute;transform:translateX(-50%);white-space:nowrap;text-align:center;font-size:12.5px;line-height:1.25;color:#3D4A5C}
.trk .lb b{display:block;font-weight:700;font-size:12px;letter-spacing:.08em;color:var(--c)}
.trk .lb.up{bottom:22px}.trk .lb.dn{top:22px}
.ft{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding:16px 44px 20px 52px;border-top:1px solid #E2E8EE}
.ft .w{font-family:'Gloock',Georgia,serif;font-size:24px}
.ft span{font-weight:600;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:#1F5F86}
"""


def esc(s):
    return s  # content is authored here, entities included deliberately


def ring(days, label):
    circ = 2 * 3.14159 * 76
    frac = min(1, days / 90)
    return f'''<div class="ring"><svg viewBox="0 0 176 176"><defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#7A4FA0"/><stop offset=".5" stop-color="#3E6491"/><stop offset="1" stop-color="#1D9E75"/></linearGradient></defs>
      <circle cx="88" cy="88" r="76" fill="none" stroke="#ECEAF5" stroke-width="13"/>
      <circle cx="88" cy="88" r="76" fill="none" stroke="url(#rg)" stroke-width="13" stroke-linecap="round"
        stroke-dasharray="{circ * frac:.1f} {circ:.1f}"/></svg>
      <div class="n"><div><b>{days}</b><span>{label}</span></div></div></div>'''


def bars(rows, lo, hi, fmt, status=None):
    out = []
    for i, r in enumerate(rows):
        k, a, b = r[0], r[1], r[2]
        c = r[3] if len(r) > 3 else BAR[i % 4]
        x0 = (a - lo) / (hi - lo) * 100 if b is not None else 0
        x1 = (b - lo) / (hi - lo) * 100 if b is not None else (a - lo) / (hi - lo) * 100
        x0, x1 = max(0, x0), min(100, x1)
        if b is not None and x1 - x0 < 4:  # point estimate: a short marker, not a hairline
            x0, x1 = max(0, x1 - 4), x1
        lab = fmt(a, b)
        inside = x1 > 72 and (x1 - x0) > 18
        pos = f"right:{100 - x1 + 1.5:.1f}%;color:#fff" if inside else f"left:{x1 + 1.5:.1f}%;color:#0F1B2D"
        st = f'<span class="st" style="color:{r[4]}">{r[5]}</span>' if len(r) > 5 else ""
        out.append(f'<div class="br"><div class="k">{k}</div><div class="tr"><i style="left:{x0:.1f}%;width:{x1 - x0:.1f}%;background:{c}"></i>'
                   f'<em style="{pos}">{lab}</em>{st}</div></div>')
    return '<div class="bars">' + "".join(out) + "</div>"


def page(d):
    ev = "".join(
        f'<li style="--c:{INK[t]}"><time>{dt}</time><span class="ev"><span class="tag">{t}</span>{txt}</span>'
        f'<span class="dd">{"DAY 0" if n == 0 else f"+{n} DAYS"}</span></li>' for n, dt, t, txt in d["events"])
    span = d["events"][-1][0]
    kp = "".join(f'<div class="kp"><div class="ml">{k}</div><b>{v}</b></div>' for k, v in d["kpis"])
    ppl = "".join(f'<div class="pp"><div class="av"></div><div><div class="rd"></div><b>{r}</b><small>{f}</small><span class="deg">{g}</span></div></div>'
                  for r, f, g in d["contacts"])
    cols = min(3, len(d["contacts"]))
    # Head start track: every event on one axis, filled from our flag to the moment the market caught up.
    pts = []
    for i, (n, dt, t, txt) in enumerate(d["events"]):
        x = n / span * 100
        side = "up" if i % 2 == 0 else "dn"
        al = "translateX(0)" if x < 6 else ("translateX(-100%)" if x > 94 else "translateX(-50%)")
        short = d.get("short", {}).get(n, t.title())
        pts.append(f'<span class="pt" style="left:{x:.1f}%;--c:{INK[t]}"></span>'
                   f'<span class="lb {side}" style="left:{x:.1f}%;transform:{al};--c:{INK[t]}"><b>{"DAY 0" if n == 0 else f"+{n}"}</b>{short}</span>')
    fill = d["days"] / span * 100
    hs = (f'<div class="hs"><div class="top2"><div><div class="ml">The head start</div><div class="big">{d["hs"]}</div></div>'
          f'<div class="days">{d["days"]} days &middot; {d["hs_vs"]}</div></div>'
          f'<div class="trk"><span class="fill" style="width:{fill:.1f}%"></span>{"".join(pts)}</div></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{d['co']} proof card</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Hanken+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}.ppl{{grid-template-columns:repeat({cols},1fr)}}</style></head><body><div class="card">
<div class="hd"><span class="flag">{FLAG[d['cty']]}</span><span class="dot"></span><span class="ml t">We saw it first &middot; captured {d['captured']}</span>
  <span class="ml strap">{d['strap']}</span><span class="ml chip">{d['chip']}</span></div>
<div class="bd">
  <div class="top"><div>
    <div class="co">{d['co']}</div><div class="ml loc">{d['loc']}</div>
    <div class="pair"><div class="mark">{d['mark_a']}</div><span class="arrow">&#10230;</span><div class="mark">{d['mark_b']}</div>
      <span class="ml deal">{d['deal_k']}<b>{d['deal_v']}</b></span></div>
  </div>{ring(d['days'], d['ring_label'])}</div>
  <div><h1>{d['h1']}</h1><p class="stand">{d['stand']}</p><div class="meta">{d['sources']}</div></div>
  <div><div class="sqh"><span class="ml l">We sequenced {len(d['events'])} events across {span} days</span><span class="ml r">{d['days']} days ahead</span></div>
    <ul class="seq">{ev}</ul></div>
  {hs}
  <div class="duo"><div class="pn a"><div class="ml">{d['left_title']}</div>{d['left']}<div class="note">{d['left_note']}</div></div>
    <div class="pn b"><div class="ml">{d['right_title']}</div>{d['right']}<div class="note">{d['right_note']}</div></div></div>
  <div class="kpis">{kp}</div>
  <div class="route"><div class="h"><span class="ml">Route in &middot; who to call</span><span>Named on {d['captured']} &middot; redacted here</span></div>
    <div class="ppl">{ppl}</div></div>
</div>
<div class="ft"><div class="w">StrategyAI</div><span>Win the mandate while it&rsquo;s still forming</span><span>strategyai.co.uk</span></div>
</div></body></html>"""


def logo(n, alt):
    return f'<img src="../out/logos/{n}.svg" alt="{alt}">'

gbpm = lambda a, b: f"&pound;{a:g}&ndash;{b:g}m"
eurm = lambda a, b: f"&euro;{a:g}&ndash;{b:g}m"
def pence(a, b): return f"{a:g}p"
def gbpbn(a, b): return f"&pound;{a:g}bn"
def gbpbn_rng(a, b): return f"&pound;{a:g}&ndash;{b:g}bn" if b is not None and b != a else f"~&pound;{a:g}bn"
CORAL, GREEN = "#C0643F", "#14795A"


def checklist(rows):
    return '<div class="chk">' + "".join(
        f'<div><span style="color:{GREEN if ok else CORAL};font-weight:700;font-size:18px">{"&#10003;" if ok else "&#10007;"}</span>'
        f'<span><b>{a}</b><small>{b}</small></span></div>' for ok, a, b in rows) + "</div>"


def holders(rows):
    return '<div class="hold">' + "".join(
        f'<div><span><span class="nm">{a}</span><small>{b}</small></span><span class="pill" style="background:{c}">{t}</span></div>'
        for a, b, t, c in rows) + "</div>"


CARDS = {
 "easyjet": dict(
    co="easyJet", cty="GB", loc="United Kingdom &middot; Industrials", strap="Contested bid", chip="53 days ahead",
    captured="30 May 2026", days=53, ring_label="days ahead<br>of the FT",
    mark_a=logo("apollo_global_management", "Apollo"), mark_b=logo("easyjet", "easyJet"),
    deal_k="Agreed", deal_v="&pound;5.7bn",
    h1="We were reading easyJet <em>fifty-three days before the Financial Times.</em>",
    stand="On <b>30 May</b> a single tabloid line said a US firm was plotting a buyout. We logged it and began sequencing. "
          "Reuters arrived 23 days later, the FT after 53, the BBC after 68, by which point Apollo had agreed terms at "
          "<b>&pound;5.7bn</b> and the advisory window had been open for two months.",
    sources="17 linked sources &middot; every item dated and auditable",
    events=[(0, "30 May", "FLAGGED", "StrategyAI logs a US buyout approach"),
            (23, "22 Jun", "PRESS", "Reuters reports the approach"),
            (37, "6 Jul", "BID", "Terms reached at 690p a share"),
            (53, "22 Jul", "PRESS", "The Financial Times covers it"),
            (68, "6 Aug", "DEAL", "Apollo agrees &pound;5.7bn; the BBC reports")],
    left_title="The bid ladder we tracked",
    left=bars([("3 Jun", 403, None, "#A9BACB", CORAL, "REJECTED"), ("22 Jun", 625, None, "#5B84A8", CORAL, "REJECTED"),
               ("6 Jul", 690, None, "#1D9E75", GREEN, "AGREED")], 0, 760, pence),
    left_note="Castlelake raised twice and still lost it. Apollo agreed &pound;5.7bn on 6 August.",
    right_title="What this work has paid",
    right=bars([("Bain &middot; 28w", 9, 16), ("McKinsey &middot; 24w", 8, 14), ("O. Wyman &middot; 20w", 6, 10), ("R. Berger &middot; 18w", 5, 9)], 0, 18, gbpm),
    right_note="Four precedent airline mandates. Two went to firms you compete with every week.",
    kpis=[("Bidders tracked", "Castlelake, then Apollo"), ("Premium", "73% to undisturbed"),
          ("Mandate shape", "Defence, then integration"), ("Evidence", "17 items &middot; 82 confidence")],
    contacts=[("Chief Executive, easyJet", "Leads the board response", "2nd degree"),
              ("Chief Financial Officer", "Owns valuation defence", "2nd degree"),
              ("Chairman", "Commissions independent advice", "2nd degree")]),
 "bodycote": dict(
    co="Bodycote", cty="GB", loc="United Kingdom &middot; Industrials", strap="Withdrawn bid", chip="85 days ahead",
    captured="8 Jun 2026", days=85, ring_label="days before<br>the deal",
    mark_a="VERITAS", mark_b="BODYCOTE", deal_k="Agreed at 940p", deal_v="&pound;1.65bn",
    h1="Apollo walked away from Bodycote. <em>We read that as the opening, not the close.</em>",
    stand="On <b>8 June</b> Apollo pulled its &pound;1.5bn bid and the market moved on. We did not: a withdrawn offer leaves a board "
          "that has already run a process and shareholders who have already seen a price. By <b>5 August</b> CVC and Veritas had both bid. "
          "On <b>1 September</b> Veritas won the board at 940p, eighty-five days after the bid that failed.",
    sources="11 linked sources &middot; Bloomberg, FT, PE Wire, Investegate",
    events=[(0, "8 Jun", "FLAGGED", "Apollo pulls its &pound;1.5bn bid; we stay on it"),
            (50, "28 Jul", "COMPANY", "Bodycote pushes ahead with a streamlining plan"),
            (58, "5 Aug", "BID", "CVC and Veritas both bid"),
            (85, "1 Sep", "DEAL", "Veritas wins the board at 940p")],
    left_title="The bid ladder we tracked",
    left=bars([("Apollo", 1.5, None, "#A9BACB", CORAL, "WITHDRAWN 8 JUN"), ("CVC / Veritas", 1.6, None, "#5B84A8", "#3E6491", "BIDS 5 AUG"),
               ("Veritas", 1.65, None, "#1D9E75", GREEN, "AGREED")], 1.3, 1.72, gbpbn),
    left_note="Axis starts at &pound;1.3bn to show the escalation. &pound;1.85bn including debt.",
    right_title="What this work has paid",
    right=bars([("McKinsey &middot; 16w", .8, 1.4), ("Bain &middot; 14w", .7, 1.3), ("AlixPartners &middot; 20w", .6, 1.2), ("O. Wyman &middot; 12w", .5, .9)], 0, 1.6, gbpm),
    right_note="Four precedent industrial performance mandates. Two went to firms you compete with every week.",
    kpis=[("Bidders tracked", "Apollo, then CVC and Veritas"), ("Outcome", "Veritas won, CVC lost"),
          ("Mandate shape", "Performance, then integration"), ("Evidence", "11 items &middot; 12&ndash;20 weeks")],
    contacts=[("Chief Executive, Bodycote plc", "Leads the streamlining programme under board pressure", "2nd degree"),
              ("Chief Financial Officer", "Owns capital allocation and portfolio rationalisation", "2nd degree")]),
 "atg-entertainment": dict(
    co="ATG Entertainment", cty="GB", loc="United Kingdom &middot; Consumer &amp; Retail", strap="Sponsor exit", chip="82 days ahead",
    captured="21 May 2026", days=82, ring_label="days before<br>the deal",
    mark_a="MARI", mark_b="ATG", deal_k="Scale we stated on day one", deal_v="&pound;4bn+",
    h1="We named the seller and the price. <em>The buyer did not surface for another thirty-four days.</em>",
    stand="On <b>21 May</b> we recorded Providence Equity Partners positioning ATG Entertainment for a sale above &pound;4bn: "
          "a named sponsor, a stated scale, a dated process. MARI was not reported as the buyer until <b>24 June</b>. "
          "The definitive agreement followed on <b>11 August</b>, eighty-two days after we put it in front of partners.",
    sources="8 linked sources &middot; PE Wire, Deadline, company statement",
    events=[(0, "21 May", "FLAGGED", "Seller named: Providence positions ATG above &pound;4bn"),
            (34, "24 Jun", "PRESS", "MARI first reported as the buyer"),
            (82, "11 Aug", "DEAL", "Definitive agreement signed")],
    left_title="What we had on day one",
    left=checklist([(True, "The seller, by name", "Providence Equity Partners"), (True, "The scale, stated", "Above &pound;4bn"),
                    (True, "The stage of the process", "Positioning for sale, not testing interest"),
                    (False, "The buyer", "Unknown for another 34 days")]),
    left_note="Three of the four facts a partner needs, on day one.",
    right_title="Comparable exits, and who got the work",
    right=bars([("Bain &middot; 14w", 2.8, None), ("McKinsey &middot; 10w", 1.5, None), ("Deloitte &middot; 12w", .8, None), ("PwC &middot; 8w", 5.0, None)], 0, 5.4, gbpbn),
    right_note="Vendor diligence and exit readiness on four comparable entertainment exits. Every one went to a firm you know.",
    kpis=[("Sponsor", "Providence Equity Partners"), ("Buyer", "MARI"),
          ("Mandate shape", "Vendor diligence, then PMI"), ("Evidence", "8 items &middot; 10&ndash;18 weeks")],
    contacts=[("Chief Executive, ATG", "Leads management presentations to buyers", "2nd degree"),
              ("Managing Director, sponsor", "Controls sell-side mandate allocation", "2nd degree"),
              ("Chief Financial Officer", "Owns the data room and vendor diligence", "3rd degree")]),
 "gamma": dict(
    co="Gamma Communications", cty="GB", loc="United Kingdom &middot; TMT", strap="Take-private", chip="39 days ahead",
    captured="24 Jul 2026", days=39, ring_label="days before<br>the deal",
    mark_a="EPIRIS", mark_b="GAMMA", deal_k="Agreed at 1,120p", deal_v="&pound;1.0bn",
    h1="A company buying its own shares mid-offer <em>is not a company that feels cornered.</em>",
    stand="On <b>24 July</b> Gamma was running a share buyback while a takeover offer period was live. That reads as a board that "
          "believes the price is wrong, and we flagged it. The deadline was extended, a sponsor was reported circling, and on "
          "<b>1 September</b> Epiris agreed a take-private at <b>1,120p</b>, a 53% premium.",
    sources="7 linked sources &middot; PE Wire, Investegate, Investing.com",
    events=[(0, "24 Jul", "FLAGGED", "Buyback during a live offer period: the tell"),
            (12, "5 Aug", "FILING", "Offer deadline extended"),
            (31, "24 Aug", "PRESS", "Waterland reported in talks"),
            (39, "1 Sep", "DEAL", "Epiris agrees at 1,120p, a 53% premium")],
    left_title="Two sponsors circled",
    left=holders([("Waterland", "Reported in talks &middot; 24 Aug", "Did not sign", CORAL),
                  ("Epiris", "Recommended offer &middot; 1 Sep", "Won the board", GREEN)]),
    left_note="The bidder first reported was not the bidder that signed.",
    right_title="Comparable UK telecoms take-privates",
    right=bars([("Jefferies / PwC", .95, 1.3), ("Goldman / Lazard", 1.2, 1.2), ("Rothschild", .8, 1.1), ("Deloitte", .6, .9)], .4, 1.5, gbpbn_rng),
    right_note="Gamma landed at &pound;1.0bn: mid-range for the sector, at the top of the premium range.",
    kpis=[("The tell", "Buyback in an offer period"), ("Premium", "53% to undisturbed"),
          ("Mandate shape", "Defence, then carve-out"), ("Evidence", "7 items &middot; 12&ndash;22 weeks")],
    contacts=[("Co-founder, major shareholder", "His support decides any recommended offer", "2nd degree"),
              ("Non-Executive Chairman", "Leads the independent board committee", "2nd degree"),
              ("Chief Financial Officer", "Owns the data room and adviser relationships", "2nd degree")]),
 "delivery-hero": dict(
    co="Delivery Hero", cty="DE", loc="Germany &middot; Business Services", strap="Public offer", chip="63 days ahead",
    captured="15 Jul 2026", days=63, ring_label="days before<br>the deal",
    mark_a=logo("uber", "Uber"), mark_b="DELIVERY HERO", deal_k="Agreed", deal_v="&euro;12.7bn",
    h1="Uber named its price in July. <em>The board did not agree it until September.</em>",
    stand="On <b>15 July</b> Uber put <b>&euro;41.50 a share</b> in cash on the table for Delivery Hero. We logged the price, the "
          "shareholder mechanics and the one holding that would decide it: Prosus, at roughly a fifth of the register. "
          "On <b>16 September</b> Uber agreed the deal at <b>&euro;12.7bn</b>. Sixty-three days of open window.",
    sources="Business Wire, Handelsblatt, company filings",
    events=[(0, "15 Jul", "FLAGGED", "Uber names &euro;41.50 a share in cash"),
            (16, "31 Jul", "FILING", "Formal offer published"),
            (63, "16 Sep", "DEAL", "Uber agrees at &euro;12.7bn")],
    left_title="The holding that decided it",
    left=holders([("Prosus", "~21% of the register &middot; irrevocable", "Swing voter", "#3E6491"),
                  ("Free float", "Tendered into the offer", "Followed", "#5E7389")]),
    left_note="A public offer is a vote, not a negotiation. We tracked the register, not the rumour.",
    right_title="What integration on this scale has paid",
    right=bars([("McKinsey &middot; 24w", 4, 7), ("Bain &middot; 20w", 3, 6), ("BCG &middot; 18w", 3, 5), ("O. Wyman &middot; 16w", 2, 4)], 0, 8, eurm),
    right_note="Four precedent platform integrations. Every one went to a firm you compete with.",
    kpis=[("The tell", "&euro;41.50 cash, named early"), ("Mechanics", "Irrevocables from the anchor"),
          ("Mandate shape", "PMI and market separation"), ("Window", "16&ndash;28 weeks")],
    contacts=[("Chief Executive, Delivery Hero", "Leads shareholder engagement and transition", "2nd degree"),
              ("Chief Financial Officer", "Owns synergy modelling and carve-out structuring", "2nd degree"),
              ("SVP Delivery, acquirer", "Accountable for integration and synergy delivery", "2nd degree")]),
 "pinewood": dict(
    co="Pinewood Technologies", cty="GB", loc="United Kingdom &middot; TMT", strap="Take-private", chip="23 days ahead",
    captured="27 Jul 2026", days=23, ring_label="days before<br>the offer",
    mark_a="RIDGEVIEW", mark_b="PINEWOOD", deal_k="Proposal we logged", deal_v="&pound;545m",
    h1="A &pound;545m proposal on 27 July. <em>The formal offer landed twenty-three days later.</em>",
    stand="On <b>27 July</b> we recorded a &pound;545m proposal from Ridgeview Partners for Pinewood Technologies. On <b>19 August</b> "
          "the Rule 2.7 announcement arrived under the name <b>U.K. Piston Bidco</b>, the Ridgeview vehicle. Anyone watching for "
          "&ldquo;Ridgeview&rdquo; in an RNS would have missed it.",
    sources="PE Wire, Investegate Rule 2.7 RNS",
    events=[(0, "27 Jul", "FLAGGED", "Ridgeview proposes &pound;545m"),
            (23, "19 Aug", "DEAL", "Rule 2.7 offer via U.K. Piston Bidco"),
            (60, "25 Sep", "VOTE", "Shareholder meeting to approve")],
    left_title="The vote was already locked",
    left=holders([("Lithia Motors", "Largest customer and strategic shareholder", "Irrevocable", GREEN),
                  ("U.K. Piston Bidco", "The Ridgeview vehicle named in the RNS", "Different name", CORAL)]),
    left_note="The buyer&rsquo;s own customer had pre-committed. That is why the offer moved in three weeks.",
    right_title="What a PE-backed software carve-out pays",
    right=bars([("McKinsey &middot; 14w", .6, 1.2), ("BCG &middot; 12w", .55, 1.0), ("Bain &middot; 10w", .5, .9), ("O. Wyman &middot; 12w", .45, .8)], 0, 1.4, gbpm),
    right_note="Four precedent operating-model mandates on PE-backed UK software assets.",
    kpis=[("Sponsor", "Ridgeview Partners"), ("Vehicle", "U.K. Piston Bidco"),
          ("Mandate shape", "Day 1 readiness, 100-day plan"), ("Evidence", "10 items &middot; 10&ndash;16 weeks")],
    contacts=[("Chief Executive, Pinewood", "Transitions into the PE-backed entity", "2nd degree"),
              ("President &amp; CEO, anchor shareholder", "Holds the irrevocable and the commercial relationship", "2nd degree")]),
}

# The head start: the headline, what it was measured against, and short labels for the track.
HEAD = {
    "easyjet": ("Partners had <em>fifty-three days</em> before the FT.", "ahead of the FT",
                {0: "We flag it", 23: "Reuters", 37: "690p terms", 53: "FT", 68: "Apollo agrees"}),
    "bodycote": ("<em>Eighty-five days</em> from a failed bid to a signed one.", "ahead of the deal",
                 {0: "Apollo walks", 50: "Streamlining", 58: "Two bids", 85: "Veritas wins"}),
    "atg-entertainment": ("<em>Eighty-two days</em> from named seller to signed deal.", "ahead of the deal",
                          {0: "Seller named", 34: "Buyer reported", 82: "Signed"}),
    "gamma": ("<em>Thirty-nine days</em> from the tell to the agreed offer.", "ahead of the deal",
              {0: "The buyback", 12: "Deadline extended", 31: "Waterland", 39: "Epiris agrees"}),
    "delivery-hero": ("<em>Sixty-three days</em> of open window before the board agreed.", "ahead of the deal",
                      {0: "Price named", 16: "Formal offer", 63: "Board agrees"}),
    "pinewood": ("<em>Twenty-three days</em> before the offer landed, under another name.", "ahead of the offer",
                 {0: "Proposal", 23: "Rule 2.7 offer", 60: "Shareholder vote"}),
}
for _k, (_h, _v, _s) in HEAD.items():
    CARDS[_k].update(hs=_h, hs_vs=_v, short=_s)

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    for name, d in CARDS.items():
        if only and name != only: continue
        f = os.path.join(OUT, f"{name}.html")
        open(f, "w", encoding="utf-8").write(page(d))
        png = os.path.join(OUT, f"{name}-proof.png")
        if os.path.exists(png): os.remove(png)
        import time
        for attempt in range(3):
            subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                            f"--user-data-dir={os.path.join(OUT, 'edge-prof')}",
                            "--window-size=1200,1600", "--virtual-time-budget=6000", f"--screenshot={png}", "file:///" + f.replace("\\", "/")],
                           capture_output=True, timeout=120)
            for _ in range(20):
                if os.path.exists(png): break
                time.sleep(0.5)
            if os.path.exists(png): break
        print(name, "ok" if os.path.exists(png) else "MISSING")
