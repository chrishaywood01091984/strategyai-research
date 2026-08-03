"""Build the cream catch cards from cards_cream.json using _cream_template.html.

The template is the finished Delivery Hero card with its content swapped for slots,
so every card is guaranteed identical in layout and only the facts differ.

Render each at 1200x1600 with Edge headless, force-device-scale-factor 2.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = open(os.path.join(HERE, "_cream_template.html"), encoding="utf-8").read()

DIAL = """<div class="dial">
      <svg width="112" height="112" viewBox="0 0 112 112">
        <circle cx="56" cy="56" r="45" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="9"/>
        <circle cx="56" cy="56" r="45" fill="none" stroke="{colour}" stroke-width="9"
                stroke-linecap="round" stroke-dasharray="{dash} 283" transform="rotate(-90 56 56)"/>
        <text class="v" x="56" y="54" text-anchor="middle">{value}</text>
        <text class="u" x="56" y="70" text-anchor="middle">{unit}</text>
      </svg><p>{caption}</p>
    </div>"""

STEP = """<div class="step">
      <div class="no">{no}</div>
      <h6>{head}</h6>
      <div class="when">{when}</div>
      <p>{body}</p>
    </div>"""

WIN = """<div class="win">
        <div class="name">{name}</div>
        <div class="window">{window}</div>
        <div class="bar"><i style="left:{left}%;width:{width}%"></i></div>
      </div>"""

PERSON = """<div class="person"><div class="redact"></div><div class="redact e"></div>
        <div class="role">{role}</div><div class="org">{org}</div></div>"""


def events_html(evs):
    out = []
    for e in evs:
        x, kind = e["x"], e.get("kind", "")
        cls = {"flag": "n flag", "deal": "n deal"}.get(kind, "n")
        out.append(f'<div class="{cls}" style="left:{x}px"></div>')
        if e["side"] == "above":
            out.append(f'<div class="stem" style="left:{x}px;top:158px;height:38px"></div>')
        else:
            col = {"flag": "var(--gold)", "deal": "rgba(255,255,255,.5)"}.get(
                kind, "rgba(201,168,76,.34)")
            top = 209 if kind == "flag" else (210 if kind == "deal" else 203)
            h = 30 if kind == "flag" else (29 if kind == "deal" else 32)
            out.append(f'<div class="stem" style="left:{x}px;top:{top}px;height:{h}px;'
                       f'background:{col}"></div>')
        style = f'left:{e.get("lx", x)}px;top:{e["top"]}px'
        if e.get("width"):
            style += f';width:{e["width"]}px'
        if e.get("align"):
            style += f';text-align:{e["align"]}'
        sc = ' style="color:var(--gold)"' if kind == "flag" else ''
        out.append(
            f'<div class="lbl{" hero" if kind in ("flag","deal") else ""}" style="{style}">'
            f'<div class="d">{e["date"]}</div><div class="t">{e["text"]}</div>'
            f'<div class="s"{sc}>{e["src"]}</div></div>')
    return "\n    ".join(out)


if __name__ == "__main__":
    spec_all = json.load(open(os.path.join(HERE, "cards_cream.json"), encoding="utf-8"))
    for name, c in spec_all.items():
        html = TPL.format(
            dials="".join(DIAL.format(**d) for d in c["dials"]),
            events=events_html(c["events"]),
            steps="".join(STEP.format(**s) for s in c["steps"]),
            wins="".join(WIN.format(**w) for w in c["wins"]),
            people="".join(PERSON.format(**p) for p in c["people"]),
            **c["meta"])
        open(os.path.join(HERE, f"{name}-cream.html"), "w", encoding="utf-8").write(html)
        print("wrote", name + "-cream.html")
