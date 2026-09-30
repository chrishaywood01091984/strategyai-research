"""Restyle the six pre-mandate dossier cards to the site palette.

Gloock + Hanken Grotesk, pure white sheet, dark blue #0F2A44 in place of gold,
green for the outcome, no cream. Company marks keep their own brand colours.
Writes out/<name>.html next to this script.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"atg": "atg-entertainment", "bodycote": "bodycote", "deliveryhero": "delivery-hero",
         "easyjet": "easyjet", "gamma": "gamma", "pinewood": "pinewood"}

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Hanken+Grotesk:'
             'wght@300;400;500;600;700&display=swap" rel="stylesheet">')

SUBS = [
    (r'<link href="https://fonts\.googleapis\.com/css2\?family=Playfair[^>]*>', FONT_LINK),
    (r'--bg:#F2EEE6', '--bg:#FFFFFF'),
    (r'--panel:#FFFFFF', '--panel:#F7F9FB'),
    (r'#0D1B2A', '#0F1B2D'),
    (r'#C9A84C', '#0F2A44'), (r'#9A7C23', '#0F2A44'),
    (r'rgba\(201,\s*168,\s*76', 'rgba(15,42,68'),
    (r'#0F8C82', '#1D9E75'), (r'rgba\(15,\s*140,\s*130', 'rgba(29,158,117'),
    (r'#7A5A8C', '#7F9BB8'),
    (r'#5E6E7E', '#5B6878'),
    (r'h1 em\{font-style:italic;color:var\(--gold-ink\)\}', 'h1 em{font-style:normal;color:#4A6F94}'),
    (r"'Playfair Display',Georgia,serif", "'Gloock',Georgia,serif"),
    (r"'DM Mono','Courier New',monospace", "'Hanken Grotesk',system-ui,sans-serif"),
    (r"'Libre Baskerville',Georgia,serif", "'Hanken Grotesk',system-ui,sans-serif"),
    (r'Playfair Display', 'Gloock'),
    (r'DM Mono, monospace', 'Hanken Grotesk, sans-serif'),
    (r'DM Mono', 'Hanken Grotesk'),
    (r'font-family:var\(--fb\);overflow:hidden\}',
     'font-family:var(--fb);overflow:hidden;font-synthesis:none;font-variant-numeric:tabular-nums}'),
]

os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
for src, name in NAMES.items():
    s = open(os.path.join(HERE, f"card-{src}.html"), encoding="utf-8").read()
    for pat, rep in SUBS:
        s = re.sub(pat, rep, s, flags=re.I)
    left = [w for w in ("Playfair", "DM Mono", "Baskerville", "C9A84C", "9A7C23", "F2EEE6")
            if w.lower() in s.lower()]
    open(os.path.join(HERE, "out", f"{name}.html"), "w", encoding="utf-8").write(s)
    print(name, "leftover:", left or "none")
