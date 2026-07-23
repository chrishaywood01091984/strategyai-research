/* StrategyAI · LinkedIn security/trust post (single 1080x1350 image)
 * Honest framing (confirmed 2026-07-17): infrastructure-only, no cert badges.
 * Claims: certified infrastructure (SOC2/ISO cloud), ICO registered, role-based
 * access, public-source intelligence. NO "zero data retention", NO "no model
 * training" (unconfirmed), NO third-party badge logos.
 * Fonts via Google Fonts so it renders in CI. render.js turns html -> png.
 */
const fs = require("fs");
const path = require("path");
const OUT = path.join(__dirname, "html");
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const fontImport = `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=DM+Mono:wght@400;500&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');`;

const icons = {
  shield: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4-3 7-7 8-4-1-7-4-7-8V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>`,
  doc: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/><path d="M9.5 14l1.5 1.5 3.5-3.5"/></svg>`,
  lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/><circle cx="12" cy="15" r="1.3"/></svg>`,
  globe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.2"/><path d="M3.8 12h16.4"/><path d="M12 3.8c2.6 2.3 2.6 14.1 0 16.4"/><path d="M12 3.8c-2.6 2.3-2.6 14.1 0 16.4"/></svg>`,
};

const cards = [
  { icon: "shield", title: "Certified infrastructure", sub: "Runs on SOC 2 and ISO 27001 certified cloud." },
  { icon: "doc",    title: "ICO registered",           sub: "On the UK data protection register." },
  { icon: "lock",   title: "Role-based access",        sub: "You see only your own accounts and sectors." },
  { icon: "globe",  title: "Public-source intelligence", sub: "Built on public market signals, not your confidential data." },
];

const cardHtml = cards.map(c => `
  <div class="card">
    <div class="ic">${icons[c.icon]}</div>
    <div class="ct">${c.title}</div>
    <div class="cs">${c.sub}</div>
  </div>`).join("");

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
${fontImport}
*{margin:0;padding:0;box-sizing:border-box;}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:#0d1b2a;color:#e8edf3;font-family:'Libre Baskerville',Georgia,serif;}
.bg{position:absolute;inset:0;}
.bg::before{content:'';position:absolute;inset:0;background:radial-gradient(120% 70% at 82% 4%, rgba(201,168,76,.16), transparent 55%),radial-gradient(90% 60% at 6% 100%, rgba(31,54,84,.6), transparent 60%);}
.frame{position:absolute;inset:48px;border:1px solid rgba(201,168,76,.28);}
.card-wrap{position:absolute;inset:0;padding:100px 92px;display:flex;flex-direction:column;height:100%;}
.brandrow{display:flex;align-items:center;justify-content:space-between;}
.wordmark{font-family:'Playfair Display';font-size:34px;font-weight:700;color:#f3f1ea;}
.wordmark em{font-style:normal;color:#c9a84c;}
.tag{font-family:'DM Mono';font-size:14px;letter-spacing:3px;text-transform:uppercase;color:#9fb0c2;}
.eyebrow{font-family:'DM Mono';font-weight:500;font-size:18px;letter-spacing:5px;text-transform:uppercase;color:#c9a84c;margin-top:72px;}
.h1{font-family:'Playfair Display';font-weight:800;font-size:72px;line-height:1.05;letter-spacing:-1px;color:#f3f1ea;margin-top:26px;}
.h1 em{font-style:italic;color:#c9a84c;}
.lede{font-family:'Libre Baskerville';font-size:24px;line-height:1.55;color:#aebccb;margin-top:26px;max-width:800px;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:56px;}
.card{border:1px solid rgba(201,168,76,.28);background:linear-gradient(160deg,rgba(21,42,64,.9),rgba(17,35,54,.9));border-radius:18px;padding:36px 34px;min-height:250px;display:flex;flex-direction:column;}
.ic{width:60px;height:60px;color:#c9a84c;margin-bottom:26px;}
.ic svg{width:100%;height:100%;}
.ct{font-family:'Playfair Display';font-weight:700;font-size:36px;line-height:1.1;color:#f3f1ea;}
.cs{font-family:'Libre Baskerville';font-size:20px;line-height:1.5;color:#9fb0c2;margin-top:14px;}
.foot{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;padding-top:44px;}
.foot .fl{font-family:'DM Mono';font-size:15px;letter-spacing:1.5px;text-transform:uppercase;color:#62788e;line-height:1.7;}
.foot .fl b{color:#9fb0c2;font-weight:500;}
</style></head><body>
<div class="slide"><div class="bg"></div><div class="frame"></div>
  <div class="card-wrap">
    <div class="brandrow"><div class="wordmark">Strategy<em>AI</em></div><div class="tag">Trust &amp; Security</div></div>
    <div class="eyebrow">Security, by design</div>
    <div class="h1">Protecting what<br>partners <em>share with us</em>.</div>
    <div class="lede">Your accounts, sectors, and watchlists stay private. Here is how.</div>
    <div class="grid">${cardHtml}</div>
    <div class="foot">
      <div class="fl">Built on <b>SOC 2 &amp; ISO 27001 certified infrastructure</b><br>ICO registered · GDPR-aligned data handling</div>
      <div class="wordmark" style="font-size:26px">Strategy<em>AI</em></div>
    </div>
  </div>
</div></body></html>`;

fs.writeFileSync(path.join(OUT, "01_security.html"), html);
console.log("wrote security post html to " + OUT);
