"""Check the cream cards for label collisions on the timeline rail.

The Bodycote card shipped with the 28 July label sitting on top of the
StrategyAI flag. That happened because label positions are hand-set pixel values
and I placed them by eye. This computes the actual boxes from the CSS geometry
and reports every overlap, so the layout is checked rather than guessed.

Geometry, from _cream_template.html:
  .lbl       width 186px, transform translateX(-50%)  -> box = lx +/- 93
  .lbl.hero  width 236px                              -> box = lx +/- 118
  an explicit "width" on the event overrides both.
Labels only collide if they are on the same side of the rail.
"""
import json, os, sys

HERE = r"C:/Users/ChrisHaywood/Code/strategyai-research/catches"
# Labels live inside .tl, which is left:48 right:48 on a 1200px card, so the
# label coordinate space is 1104 wide -- not 1200. Getting this wrong is why the
# off-edge check passed on a label that was actually running off the panel.
CARD_W = 1104
EDGE = 26          # .spine sits 26px in from each edge
# .method is right:22 width:352 top:16, about 96px tall. Above-rail labels start
# at top 74, so they overlap it vertically and must stay clear of it in x.
METHOD_LEFT = CARD_W - 22 - 352
MIN_GAP = 14       # breathing room between two label boxes


def box(e):
    if e.get("width"):
        w = e["width"]
    elif e.get("kind") in ("flag", "deal"):
        w = 236
    else:
        w = 186
    cx = e.get("lx", e["x"])
    return cx - w / 2, cx + w / 2, w


def check(name, card):
    problems = []
    evs = card["events"]
    for side in ("above", "below"):
        group = [e for e in evs if e["side"] == side]
        group.sort(key=lambda e: e.get("lx", e["x"]))
        for a, b in zip(group, group[1:]):
            a0, a1, aw = box(a)
            b0, b1, bw = box(b)
            if b0 < a1 + MIN_GAP:
                problems.append(
                    f"    {side.upper():5} overlap: '{a['date']}' [{a0:.0f}-{a1:.0f}] "
                    f"vs '{b['date']}' [{b0:.0f}-{b1:.0f}] "
                    f"— need {a1 + MIN_GAP - b0:.0f}px more")
    # Off-card labels
    for e in evs:
        b0, b1, w = box(e)
        if b0 < 0:
            problems.append(f"    OFF LEFT  : '{e['date']}' starts at {b0:.0f}")
        if b1 > CARD_W:
            problems.append(f"    OFF RIGHT : '{e['date']}' ends at {b1:.0f}")
    # Above-rail labels must clear the "how the signal is built" box
    for e in evs:
        if e["side"] == "above":
            b0, b1, _ = box(e)
            if b1 > METHOD_LEFT:
                problems.append(
                    f"    METHOD BOX: '{e['date']}' ends at {b1:.0f}, "
                    f"method box starts at {METHOD_LEFT}")
    # Nodes must sit on the rail
    for e in evs:
        if not (EDGE <= e["x"] <= CARD_W - EDGE):
            problems.append(f"    NODE OFF RAIL: '{e['date']}' at x={e['x']}")
    return problems


if __name__ == "__main__":
    cards = json.load(open(os.path.join(HERE, "cards_cream.json"), encoding="utf-8"))
    only = sys.argv[1:] or list(cards)
    bad = 0
    for name in only:
        probs = check(name, cards[name])
        if probs:
            bad += 1
            print(f"  {name}: {len(probs)} problem(s)")
            print("\n".join(probs))
        else:
            print(f"  {name}: clean")
    print(f"\n{bad} card(s) with problems")
