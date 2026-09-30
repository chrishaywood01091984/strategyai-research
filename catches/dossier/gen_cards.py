"""Generate the remaining two dossier cards.

Chart bar geometry is computed from the data rather than hand-placed - three of
the first four cards shipped with bars that did not match their own axis, which
is the one defect a partner-facing chart cannot have.
"""
import io, os, sys

SP = os.path.dirname(os.path.abspath(__file__))

CSS = """
  :root{
    --bg:#F2EEE6; --panel:#FFFFFF; --ink:#0D1B2A;
    --gold:#C9A84C; --gold-ink:#9A7C23;
    --teal:#0F8C82; --coral:#CE6238; --plum:#7A5A8C; --slate:#3E6491;
    --mut:#5E6E7E; --hair:rgba(13,27,42,.16); --hair2:rgba(13,27,42,.09);
    --fp:'Playfair Display',Georgia,serif;
    --fm:'DM Mono','Courier New',monospace;
    --fb:'Libre Baskerville',Georgia,serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{width:1200px;height:1600px;background:var(--bg);color:var(--ink);
       font-family:var(--fb);overflow:hidden}
  .sheet{width:1200px;height:1600px;padding:0 54px;display:flex;flex-direction:column;
         justify-content:space-between;border-top:3px solid var(--gold)}
  .lab{font-family:var(--fm);font-size:9.5px;letter-spacing:.24em;text-transform:uppercase}
  .ttl{font-family:var(--fp);font-weight:700;font-size:21px}
  .panel{background:var(--panel);border:1px solid var(--hair2);border-radius:3px;
         box-shadow:0 1px 2px rgba(13,27,42,.04)}
  .mast{display:flex;justify-content:space-between;align-items:baseline;
        padding:18px 0 13px;border-bottom:1px solid var(--hair)}
  .mast .l{color:var(--gold-ink)} .mast .r{color:var(--mut)}
  .princ{display:flex;align-items:center;gap:20px;padding:15px 0 0}
  .mark{height:50px;min-width:124px;background:var(--panel);border:1px solid var(--hair2);
        border-radius:3px;display:flex;align-items:center;justify-content:center;padding:8px 18px}
  .mark img{max-height:24px;max-width:100px;display:block}
  .mark .word{font-family:var(--fp);font-weight:700;font-size:18px;letter-spacing:.02em;white-space:nowrap}
  .arrow{font-family:var(--fm);font-size:15px;color:var(--gold-ink)}
  .princ .meta{margin-left:auto;text-align:right}
  .princ .meta .k{font-family:var(--fm);font-size:9px;letter-spacing:.17em;text-transform:uppercase;color:var(--mut)}
  .princ .meta .v{font-family:var(--fm);font-size:15px;color:var(--gold-ink);margin-top:5px}
  .lede{padding:18px 0 2px}
  h1{font-family:var(--fp);font-weight:700;font-size:43px;line-height:1.1;letter-spacing:-.012em;max-width:1040px}
  h1 em{font-style:italic;color:var(--gold-ink)}
  .stand{font-size:14px;line-height:1.72;color:var(--mut);max-width:940px;margin-top:13px}
  .stand b{color:var(--ink);font-weight:400}
  .block{margin-top:16px;padding:16px 22px 12px}
  .block .hd{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px}
  .duo{display:grid;grid-template-columns:1.15fr 1fr;gap:16px;margin-top:16px}
  .duo .panel{padding:16px 20px 13px}
  .duo .k{font-family:var(--fm);font-size:9px;letter-spacing:.17em;text-transform:uppercase;color:var(--mut)}
  .duo .note{font-family:var(--fm);font-size:9.5px;color:var(--slate);margin-top:9px;line-height:1.7}
  .kv{margin-top:14px}
  .kv .r{display:flex;align-items:baseline;justify-content:space-between;gap:12px;
         padding:11px 0;border-bottom:1px solid var(--hair2)}
  .kv .r:last-child{border-bottom:none}
  .kv .nm{font-family:var(--fp);font-weight:700;font-size:18px}
  .kv .dt{font-family:var(--fm);font-size:9px;letter-spacing:.12em;text-transform:uppercase;
          color:var(--mut);margin-top:4px}
  .kv .tag{font-family:var(--fm);font-size:9px;letter-spacing:.11em;text-transform:uppercase;
           border-radius:2px;padding:4px 9px;flex:none;
           color:var(--teal);border:1px solid rgba(15,140,130,.45)}
  .kv .tag.amber{color:var(--coral);border-color:rgba(206,98,56,.4)}
  .ts{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;margin-top:16px}
  .row{display:flex;justify-content:space-between;align-items:baseline;gap:14px;
       padding:7px 0;border-bottom:1px solid var(--hair2)}
  .row .k{font-family:var(--fm);font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
  .row .v{font-family:var(--fm);font-size:12px;text-align:right;font-variant-numeric:tabular-nums}
  .row .v.g{color:var(--gold-ink)}
  .route{margin-top:16px}
  .route .hd{display:flex;justify-content:space-between;align-items:baseline;
             padding-bottom:9px;border-bottom:1px solid var(--hair)}
  .cg{display:grid;gap:16px;margin-top:13px}
  .c{background:var(--panel);border:1px solid var(--hair2);border-radius:3px;padding:12px 15px}
  .rd{height:9px;border-radius:2px;background:linear-gradient(90deg,rgba(13,27,42,.34),rgba(13,27,42,.12));filter:blur(3px)}
  .rd.s{width:56%;margin-top:7px}
  .c .role{font-family:var(--fp);font-weight:700;font-size:14px;margin-top:11px;line-height:1.3}
  .c .f{font-family:var(--fm);font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-top:5px}
  .c .deg{display:inline-block;font-family:var(--fm);font-size:8px;letter-spacing:.1em;
          text-transform:uppercase;color:var(--teal);border:1px solid rgba(15,140,130,.4);
          border-radius:2px;padding:3px 7px;margin-top:8px}
  .foot{display:flex;justify-content:space-between;align-items:center;
        border-top:1px solid var(--hair);padding:12px 0 17px;margin-top:14px}
  .logo{font-family:var(--fp);font-weight:700;font-size:16px}
  .logo span{color:var(--gold-ink)}
"""

COLS = ['#C9A84C', '#7A5A8C', '#3E6491', '#0F8C82']


def comparables_svg(rows, ticks, unit, x0=150, x1=450):
    """rows: (label, lo, hi). ticks: axis values. Geometry derived from the scale."""
    lo_ax, hi_ax = ticks[0] - (ticks[1] - ticks[0]), ticks[-1]
    X = lambda v: x0 + (v - lo_ax) * (x1 - x0) / (hi_ax - lo_ax)
    out = ['<svg width="100%" height="128" viewBox="0 0 470 128">']
    out.append('        <g font-family="DM Mono, monospace" font-size="9" fill="#5E6E7E" letter-spacing="1.1">')
    for i, (lab, _, _) in enumerate(rows):
        out.append(f'          <text x="0" y="{20 + i * 28}">{lab}</text>')
    out.append('        </g>')
    out.append('        <g stroke="rgba(13,27,42,.10)" stroke-width="1">')
    for t in ticks:
        out.append(f'          <line x1="{X(t):.0f}" y1="6" x2="{X(t):.0f}" y2="112"/>')
    out.append('        </g>')
    labels = []
    for i, (_, lo, hi) in enumerate(rows):
        y = 8 + i * 28
        x, w = X(lo), X(hi) - X(lo)
        out.append(f'        <rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="14" rx="2" fill="{COLS[i]}"/>')
        labels.append(f'          <text x="{x + w + 8:.0f}" y="{y + 11}">{unit(lo)}&ndash;{unit(hi)}</text>')
    out.append('        <g font-family="DM Mono, monospace" font-size="10" fill="#0D1B2A">')
    out += labels
    out.append('        </g>')
    out.append('        <g font-family="DM Mono, monospace" font-size="8" fill="#5E6E7E" letter-spacing="1">')
    for t in ticks:
        out.append(f'          <text x="{X(t):.0f}" y="124">{unit(t)}</text>')
    out.append('        </g></svg>')
    return '\n'.join(out)


def timeline_svg(nodes, span_days, x0=60, x1=967):
    """nodes: (day, kind, colour, top_lines, bottom_lines) - kind 'big' or 'small'."""
    X = lambda d: x0 + d * (x1 - x0) / span_days
    o = ['<svg width="1044" height="150" viewBox="0 0 1044 150">',
         '      <defs><linearGradient id="fade" gradientUnits="userSpaceOnUse" '
         f'x1="{x0}" y1="0" x2="{x1}" y2="0">',
         '        <stop offset="0" stop-color="#C9A84C"/><stop offset="1" stop-color="#0F8C82"/>'
         '</linearGradient></defs>',
         f'      <line x1="{x0}" y1="104" x2="1000" y2="104" stroke="rgba(13,27,42,.14)" stroke-width="1"/>',
         f'      <line x1="{x0}" y1="104" x2="{x1}" y2="104" stroke="url(#fade)" stroke-width="4" '
         'stroke-linecap="round"/>']
    for day, kind, col, top, bot in nodes:
        x = X(day)
        r = 9 if kind == 'big' else 6
        o.append(f'      <circle cx="{x:.0f}" cy="104" r="{r}" fill="{col}"/>')
        if kind == 'big':
            o.append(f'      <circle cx="{x:.0f}" cy="104" r="16" fill="none" '
                     f'stroke="{col}55" stroke-width="1.5"/>')
        anchor = 'start' if day == 0 else ('end' if day >= span_days else 'middle')
        ax = x if anchor == 'middle' else (x0 if anchor == 'start' else 1000)
        for j, (txt, size, colour, font) in enumerate(top):
            o.append(f'      <text x="{ax:.0f}" y="{46 + j * 20}" text-anchor="{anchor}" '
                     f'font-family="{font}" font-size="{size}" fill="{colour}" '
                     f'{"font-weight=\"700\"" if font.startswith("Playfair") else "letter-spacing=\"1.4\""}>{txt}</text>')
        for j, (txt, size, colour, font) in enumerate(bot):
            o.append(f'      <text x="{ax:.0f}" y="{132 + j * 14}" text-anchor="{anchor}" '
                     f'font-family="{font}" font-size="{size}" fill="{colour}" '
                     f'{"font-weight=\"700\"" if font.startswith("Playfair") else "letter-spacing=\"1.2\""}>{txt}</text>')
    o.append('    </svg>')
    return '\n'.join(o)


def page(d):
    contacts = '\n'.join(
        f'''      <div class="c"><div class="rd"></div><div class="rd s"></div>
        <div class="role">{r}</div><div class="f">{f}</div><div class="deg">{g}</div></div>'''
        for r, f, g in d['contacts'])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{d['co']} pre-mandate dossier</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400;1,700&family=DM+Mono:wght@400;500&family=Libre+Baskerville:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<style>{CSS}  .cg{{grid-template-columns:repeat({len(d['contacts'])},1fr)}}
</style>
</head>
<body>
<div class="sheet">
  <div class="mast">
    <div class="lab l">Pre-mandate dossier</div>
    <div class="lab" style="letter-spacing:.18em">{d['strap']}</div>
    <div class="lab r">Captured {d['captured']}</div>
  </div>
  <div class="princ">
    <div class="mark">{d['mark_a']}</div>
    <div class="arrow">&#10230;</div>
    <div class="mark">{d['mark_b']}</div>
    <div>
      <div class="lab" style="color:var(--mut)">Acquirer &rarr; target</div>
      <div style="font-family:var(--fm);font-size:12px;margin-top:6px">{d['pair']}</div>
    </div>
    <div class="meta"><div class="k">{d['meta_k']}</div><div class="v">{d['meta_v']}</div></div>
  </div>
  <div class="lede">
    <h1>{d['h1']}</h1>
    <p class="stand">{d['stand']}</p>
  </div>
  <div class="panel block">
    <div class="hd">
      <div class="lab" style="color:var(--gold-ink)">{d['tl_title']}</div>
      <div class="lab" style="color:var(--mut)">{d['tl_range']}</div>
    </div>
    {d['timeline']}
  </div>
  <div class="duo">
    <div class="panel">
      <div class="k">{d['comp_title']}</div>
      {d['comparables']}
      <div class="note">{d['comp_note']}</div>
    </div>
    <div class="panel">
      <div class="k">{d['side_title']}</div>
      <div class="kv">{d['side_rows']}</div>
      <div class="note">{d['side_note']}</div>
    </div>
  </div>
  <div class="ts">
    <div>{d['ts_left']}</div>
    <div>{d['ts_right']}</div>
  </div>
  <div class="route">
    <div class="hd"><div class="ttl">Route in</div>
      <div class="lab" style="color:var(--mut)">Named on {d['captured']} &middot; redacted here</div></div>
    <div class="cg">
{contacts}
    </div>
  </div>
  <div class="foot">
    <div class="logo">Strategy<span>AI</span></div>
    <div class="lab" style="color:var(--mut)">{d['sources']}</div>
    <div class="lab" style="color:var(--mut)">strategyai.co.uk</div>
  </div>
</div>
</body>
</html>"""


def row(k, v, gold=False):
    return f'      <div class="row"><span class="k">{k}</span><span class="v{" g" if gold else ""}">{v}</span></div>'


eur = lambda v: f'&euro;{v:g}m'
gbp = lambda v: (f'&pound;{v:g}m' if v >= 1 else f'&pound;{int(v*1000)}k')

PF, DM = 'Playfair Display, serif', 'DM Mono, monospace'

DH = dict(
    co='Delivery Hero', strap='Business Services &middot; Germany &middot; Public offer',
    captured='15 Jul 2026',
    mark_a='<img src="logos/uber.svg" alt="Uber">',
    mark_b='<span class="word">DELIVERY HERO</span>',
    pair='Uber Technologies &middot; Delivery Hero SE', meta_k='Agreed consideration', meta_v='&euro;12.7bn',
    h1='Uber named its price in July. <em>The board did not agree it until September.</em>',
    stand='On <b>15 July</b> Uber put <b>&euro;41.50 a share</b> in cash on the table for Delivery Hero. '
          'We logged the price, the shareholder mechanics and the one holding that would decide it &mdash; '
          'Prosus, at roughly a fifth of the register. The formal offer followed on 31 July. '
          'On <b>16 September</b> Uber agreed the deal at <b>&euro;12.7bn</b>. Sixty-three days of open window.',
    tl_title='From price on the table to signed deal', tl_range='15 Jul &ndash; 16 Sep 2026',
    timeline=timeline_svg([
        (0, 'big', '#C9A84C',
         [('15 JUL', 10, '#9A7C23', DM), ('Uber names &euro;41.50 a share', 17, '#0D1B2A', PF),
          ('DAY 0 &middot; PRICE ON THE TABLE', 9, '#5E6E7E', DM)], []),
        (16, 'small', '#3E6491', [],
         [('FORMAL OFFER', 9.5, '#3E6491', DM), ('+16 DAYS &middot; HANDELSBLATT', 9, '#5E6E7E', DM)]),
        (63, 'big', '#0F8C82',
         [('Uber agrees at &euro;12.7bn', 15, '#0F8C82', PF),
          ('+63 DAYS &middot; 16 SEP', 9, '#5E6E7E', DM)], []),
    ], 63),
    comp_title='What integration on this scale has paid',
    comparables=comparables_svg([('McKINSEY &middot; 24W', 4, 7), ('BAIN &middot; 20W', 3, 6),
                                 ('BCG &middot; 18W', 3, 5), ('O. WYMAN &middot; 16W', 2, 4)],
                                [2, 4, 6, 8], eur),
    comp_note='Four precedent platform integrations.<br>Every one went to a firm you compete with.',
    side_title='The holding that decided it',
    side_rows='''
        <div class="r"><div><div class="nm">Prosus</div>
          <div class="dt">~21% of the register &middot; irrevocable undertaking</div></div>
          <div class="tag">Swing voter</div></div>
        <div class="r"><div><div class="nm">Free float</div>
          <div class="dt">Tendered into the offer</div></div>
          <div class="tag amber">Followed</div></div>''',
    side_note='A public offer is a vote, not a negotiation.<br>We tracked the register, not the rumour.',
    ts_left=row('The tell', '&euro;41.50 cash, named early') + row('Premium mechanics', 'Irrevocables from the anchor', True),
    ts_right=row('Mandate shape', 'PMI and market separation') + row('Evidence &middot; window', '16&ndash;28 weeks', True),
    contacts=[('Chief Executive, Delivery Hero', 'Leads shareholder engagement and transition', '2nd degree'),
              ('Chief Financial Officer', 'Owns synergy modelling and carve-out structuring', '2nd degree'),
              ('SVP Delivery, acquirer', 'Accountable for integration and synergy delivery', '2nd degree')],
    sources='Business Wire, Handelsblatt, company filings',
)

PW = dict(
    co='Pinewood Technologies', strap='TMT &middot; United Kingdom &middot; Take-private',
    captured='27 Jul 2026',
    mark_a='<span class="word">RIDGEVIEW</span>', mark_b='<span class="word">PINEWOOD</span>',
    pair='Ridgeview Partners &middot; Pinewood Technologies Group',
    meta_k='Proposal we logged', meta_v='&pound;545m',
    h1='A &pound;545m proposal on 27 July. <em>The formal offer landed twenty-three days later.</em>',
    stand='On <b>27 July</b> we recorded a &pound;545m acquisition proposal from Ridgeview Partners for '
          'Pinewood Technologies. On <b>19 August</b> the Rule 2.7 announcement arrived under the name '
          '<b>U.K. Piston Bidco</b> &mdash; the Ridgeview vehicle. Anyone watching for "Ridgeview" in an RNS '
          'would have missed it. Shareholders meet to approve on 25 September.',
    tl_title='Proposal, then the bidco', tl_range='27 Jul &ndash; 19 Aug 2026',
    timeline=timeline_svg([
        (0, 'big', '#C9A84C',
         [('27 JUL', 10, '#9A7C23', DM), ('Ridgeview proposes &pound;545m', 17, '#0D1B2A', PF),
          ('DAY 0 &middot; PE WIRE', 9, '#5E6E7E', DM)], []),
        (23, 'big', '#0F8C82',
         [('Rule 2.7 offer via Piston Bidco', 15, '#0F8C82', PF),
          ('+23 DAYS &middot; 19 AUG', 9, '#5E6E7E', DM)], []),
    ], 23),
    comp_title='What a PE-backed software carve-out pays',
    comparables=comparables_svg([('McKINSEY &middot; 14W', 0.6, 1.2), ('BCG &middot; 12W', 0.55, 1.0),
                                 ('BAIN &middot; 10W', 0.5, 0.9), ('O. WYMAN &middot; 12W', 0.45, 0.8)],
                                [0.4, 0.8, 1.2, 1.6], gbp),
    comp_note='Four precedent operating-model mandates<br>on PE-backed UK software assets.',
    side_title='The vote was already locked',
    side_rows='''
        <div class="r"><div><div class="nm">Lithia Motors</div>
          <div class="dt">Largest customer and strategic shareholder</div></div>
          <div class="tag">Irrevocable</div></div>
        <div class="r"><div><div class="nm">U.K. Piston Bidco</div>
          <div class="dt">The Ridgeview vehicle named in the RNS</div></div>
          <div class="tag amber">Different name</div></div>''',
    side_note='The buyer&rsquo;s own customer had pre-committed.<br>That is why the offer moved in three weeks.',
    ts_left=row('Sponsor', 'Ridgeview Partners, San Francisco') + row('Vehicle', 'U.K. Piston Bidco', True),
    ts_right=row('Mandate shape', 'Day 1 readiness and 100-day plan') + row('Evidence &middot; window', '10 items &middot; 10&ndash;16 weeks', True),
    contacts=[('Chief Executive, Pinewood', 'Transitions into the PE-backed entity', '2nd degree'),
              ('President &amp; CEO, anchor shareholder', 'Holds the irrevocable and the commercial relationship', '2nd degree')],
    sources='PE Wire, Investegate Rule 2.7 RNS',
)

for name, d in (('card-deliveryhero.html', DH), ('card-pinewood.html', PW)):
    path = os.path.join(SP, name)
    io.open(path, 'w', encoding='utf-8').write(page(d))
    print('wrote', name)
