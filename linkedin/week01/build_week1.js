/* StrategyAI · 10-Week LinkedIn series · WEEK 1 carousel
 * "The mandate is won before it's announced." (sector link: /market-outlook)
 * Portrait 1080x1350 document carousel. One self-contained HTML per slide + _all.html.
 * Fonts load from Google Fonts (Playfair Display / DM Mono / Libre Baskerville) so this
 * renders in CI with no local font install. render.js (puppeteer) turns html -> png + pdf.
 * Brand: navy #0d1b2a, gold #c9a84c.
 * House rules: no em dashes, EMEIA-only, action not alerts (evidence + warm intro + next step).
 */
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "html");
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const TOTAL = 9;
const URL = "research.strategyai.co.uk/market-outlook";

const fontImport = `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=DM+Mono:wght@400;500&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');`;

const baseCss = `
${fontImport}
*{margin:0;padding:0;box-sizing:border-box;}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;
  background:#0d1b2a;color:#e8edf3;font-family:'Libre Baskerville',Georgia,serif;}
.bg{position:absolute;inset:0;z-index:0;}
.bg::before{content:'';position:absolute;inset:0;
  background:radial-gradient(120% 70% at 80% 6%, rgba(201,168,76,.15), transparent 55%),
             radial-gradient(90% 60% at 8% 100%, rgba(31,54,84,.6), transparent 60%);}
.frame{position:absolute;inset:48px;border:1px solid rgba(201,168,76,.28);z-index:1;}
.card{position:absolute;inset:0;z-index:2;padding:104px 96px;display:flex;flex-direction:column;height:100%;}
.brandrow{display:flex;align-items:center;justify-content:space-between;}
.wordmark{font-family:'Playfair Display';font-size:34px;font-weight:700;letter-spacing:.5px;color:#f3f1ea;}
.wordmark em{font-style:normal;color:#c9a84c;}
.livedot{display:flex;align-items:center;gap:11px;font-family:'DM Mono';font-size:15px;letter-spacing:2.5px;color:#9fb0c2;text-transform:uppercase;}
.livedot span.d{width:9px;height:9px;border-radius:50%;background:#22c55e;box-shadow:0 0 12px #22c55e;}
.foot{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:24px;}
.pageno{font-family:'DM Mono';font-size:15px;letter-spacing:3px;color:#62788e;text-transform:uppercase;}
.swipe{font-family:'DM Mono';font-size:15px;letter-spacing:3px;color:#c9a84c;text-transform:uppercase;}
`;

function slide(inner, n, swipe){
  const foot = `<div class="foot">
      <div class="pageno">${String(n).padStart(2,"0")} / ${TOTAL}</div>
      ${swipe ? `<div class="swipe">${swipe}</div>` : `<div class="pageno">EMEIA MANDATE INTELLIGENCE</div>`}
    </div>`;
  return `<!doctype html><html><head><meta charset="utf-8"><style>${baseCss}${inner.css||""}</style></head><body>
  <div class="slide"><div class="bg"></div><div class="frame"></div>
    <div class="card">
      <div class="brandrow"><div class="wordmark">Strategy<em>AI</em></div><div class="livedot"><span class="d"></span>Live pipeline</div></div>
      ${inner.body}
      ${foot}
    </div></div></body></html>`;
}

const slides = [];

slides.push({ id:"01_cover", swipe:"Swipe →", css:`
  .kick{font-family:'DM Mono';font-weight:500;font-size:19px;letter-spacing:5px;text-transform:uppercase;color:#c9a84c;margin-top:120px;}
  .h1{font-family:'Playfair Display';font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-1.5px;color:#f3f1ea;margin-top:44px;}
  .h1 em{font-style:italic;color:#c9a84c;}
  .lede{font-family:'Libre Baskerville';font-size:27px;line-height:1.6;color:#aebccb;margin-top:52px;max-width:760px;}`,
  body:`<div class="kick">Week 1 · The timing edge</div>
    <div class="h1">The mandate<br>is won <em>before</em><br>it's announced.</div>
    <div class="lede">Why the firms that win are not pitching harder. They are arriving earlier.</div>`});

slides.push({ id:"02_public", swipe:"Swipe →", css:`
  .wrap{margin-top:auto;margin-bottom:auto;}
  .big{font-family:'Playfair Display';font-weight:800;font-size:78px;line-height:1.12;color:#f3f1ea;letter-spacing:-.5px;}
  .big em{font-style:italic;color:#c9a84c;}`,
  body:`<div class="wrap"><div class="big">By the time a deal is public, you are <em>one of five firms</em> pitching for it.</div></div>`});

slides.push({ id:"03_timing", swipe:"Swipe →", css:`
  .wrap{margin-top:auto;margin-bottom:auto;}
  .big{font-family:'Playfair Display';font-weight:800;font-size:88px;line-height:1.1;color:#f3f1ea;letter-spacing:-.5px;}
  .big em{font-style:italic;color:#c9a84c;}
  .note{font-family:'Libre Baskerville';font-size:26px;line-height:1.6;color:#aebccb;margin-top:44px;max-width:720px;}`,
  body:`<div class="wrap"><div class="big">The advantage was never the pitch.<br>It was the <em>timing</em>.</div>
    <div class="note">Before any mandate becomes public, it leaves a trail.</div></div>`});

slides.push({ id:"04_trail", swipe:"Swipe →", css:`
  .kick2{font-family:'DM Mono';font-weight:500;font-size:18px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;margin-top:96px;}
  .h2{font-family:'Playfair Display';font-weight:700;font-size:64px;line-height:1.06;color:#f3f1ea;margin-top:28px;}
  .list{margin-top:56px;display:flex;flex-direction:column;gap:0;}
  .row{display:flex;align-items:baseline;gap:28px;padding:30px 0;border-top:1px solid rgba(201,168,76,.22);}
  .row:last-child{border-bottom:1px solid rgba(201,168,76,.22);}
  .rn{font-family:'DM Mono';font-size:20px;color:#c9a84c;letter-spacing:1px;min-width:44px;}
  .rt{font-family:'Playfair Display';font-size:40px;color:#f3f1ea;line-height:1.2;}
  .rs{font-family:'Libre Baskerville';font-size:21px;color:#9fb0c2;margin-top:8px;}`,
  body:`<div class="kick2">The signals a mandate leaves</div>
    <div class="h2">Read on their own, noise.<br>Read together, a mandate forming.</div>
    <div class="list">
      <div class="row"><div class="rn">01</div><div><div class="rt">A leadership change</div><div class="rs">A new CFO or CEO arrives with a mandate to change things.</div></div></div>
      <div class="row"><div class="rn">02</div><div><div class="rt">A hiring surge</div><div class="rs">Transformation, integration and corporate development roles open up.</div></div></div>
      <div class="row"><div class="rn">03</div><div><div class="rt">Capital shifts</div><div class="rs">The structure moves. A review begins. Advisors start circling.</div></div></div>
    </div>`});

slides.push({ id:"05_where", swipe:"Swipe →", css:`
  .h2{font-family:'Playfair Display';font-weight:700;font-size:60px;line-height:1.08;color:#f3f1ea;margin-top:110px;}
  .h2 em{font-style:italic;color:#c9a84c;}
  .cols{display:flex;gap:0;margin-top:66px;border:1px solid rgba(201,168,76,.22);}
  .col{flex:1;padding:44px 40px;}
  .col+.col{border-left:1px solid rgba(201,168,76,.22);}
  .cl{font-family:'DM Mono';font-size:15px;letter-spacing:2.5px;text-transform:uppercase;color:#8aa0b6;}
  .ci{font-family:'Playfair Display';font-size:31px;color:#f3f1ea;margin-top:26px;line-height:1.5;}
  .col.gold .cl{color:#c9a84c;}`,
  body:`<div class="h2">Most of that trail sits <em>outside</em> the databases everyone reads.</div>
    <div class="cols">
      <div class="col"><div class="cl">Where everyone looks</div><div class="ci">Bloomberg.<br>Preqin.<br>The same names, at the same time.</div></div>
      <div class="col gold"><div class="cl">Where it actually is</div><div class="ci">Job posts. Filings. RNS. Trade press. Across 14 EMEIA countries.</div></div>
    </div>`});

slides.push({ id:"06_monitor", swipe:"Swipe →", css:`
  .h2{font-family:'Playfair Display';font-weight:700;font-size:62px;line-height:1.08;color:#f3f1ea;margin-top:100px;}
  .h2 em{font-style:italic;color:#c9a84c;}
  .statgrid{display:flex;flex-wrap:wrap;margin-top:70px;border-top:1px solid rgba(201,168,76,.28);border-left:1px solid rgba(201,168,76,.28);}
  .st{width:50%;padding:40px 36px;border-right:1px solid rgba(201,168,76,.28);border-bottom:1px solid rgba(201,168,76,.28);}
  .sv{font-family:'Playfair Display';font-weight:900;font-size:78px;color:#c9a84c;line-height:1;}
  .sl{font-family:'DM Mono';font-size:16px;letter-spacing:2px;text-transform:uppercase;color:#9fb0c2;margin-top:16px;}`,
  body:`<div class="h2">StrategyAI monitors it every day, and ranks what matters onto <em>one brief</em>.</div>
    <div class="statgrid">
      <div class="st"><div class="sv">1,340+</div><div class="sl">Companies monitored</div></div>
      <div class="st"><div class="sv">96+</div><div class="sl">Signal sources</div></div>
      <div class="st"><div class="sv">14</div><div class="sl">EMEIA countries</div></div>
      <div class="st"><div class="sv">06:30</div><div class="sl">Ranked brief, daily</div></div>
    </div>`});

slides.push({ id:"07_action", swipe:"Swipe →", css:`
  .kick2{font-family:'DM Mono';font-weight:500;font-size:18px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;margin-top:100px;}
  .h2{font-family:'Playfair Display';font-weight:700;font-size:60px;line-height:1.08;color:#f3f1ea;margin-top:28px;}
  .pil{margin-top:64px;display:flex;flex-direction:column;gap:0;}
  .p{padding:38px 0;border-top:1px solid rgba(201,168,76,.22);display:flex;gap:32px;align-items:baseline;}
  .p:last-child{border-bottom:1px solid rgba(201,168,76,.22);}
  .pn{font-family:'Playfair Display';font-weight:900;font-size:46px;color:#c9a84c;min-width:70px;}
  .pt{font-family:'Playfair Display';font-size:42px;color:#f3f1ea;}
  .pd{font-family:'Libre Baskerville';font-size:22px;color:#9fb0c2;margin-top:8px;line-height:1.5;}`,
  body:`<div class="kick2">Not just a signal</div>
    <div class="h2">We hand you what to do about it.</div>
    <div class="pil">
      <div class="p"><div class="pn">01</div><div><div class="pt">The evidence</div><div class="pd">The proof behind the signal, so you act with conviction.</div></div></div>
      <div class="p"><div class="pn">02</div><div><div class="pt">The warm introduction</div><div class="pd">A route into the room, to a named contact.</div></div></div>
      <div class="p"><div class="pn">03</div><div><div class="pt">The next step</div><div class="pd">The specific BD angle to open the conversation.</div></div></div>
    </div>`});

slides.push({ id:"08_cta", swipe:"Read it →", css:`
  .wrap{margin-top:auto;margin-bottom:auto;}
  .kick2{font-family:'DM Mono';font-weight:500;font-size:18px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;}
  .h2{font-family:'Playfair Display';font-weight:800;font-size:82px;line-height:1.06;color:#f3f1ea;margin-top:34px;letter-spacing:-.5px;}
  .h2 em{font-style:italic;color:#c9a84c;}
  .urlbox{margin-top:56px;border:1px solid rgba(201,168,76,.5);background:rgba(201,168,76,.08);padding:34px 40px;display:inline-block;}
  .url{font-family:'DM Mono';font-size:30px;letter-spacing:1px;color:#e8c976;}`,
  body:`<div class="wrap"><div class="kick2">Free to read this month</div>
    <div class="h2">The EMEIA<br><em>market outlook</em>.</div>
    <div class="urlbox"><div class="url">${URL}</div></div></div>`});

slides.push({ id:"09_close", swipe:"", css:`
  .wrap{margin-top:auto;margin-bottom:auto;}
  .h1{font-family:'Playfair Display';font-weight:800;font-size:96px;line-height:1.05;color:#f3f1ea;letter-spacing:-1px;}
  .h1 em{font-style:italic;color:#c9a84c;}
  .sub{font-family:'Libre Baskerville';font-size:26px;color:#aebccb;margin-top:44px;}
  .url{font-family:'DM Mono';font-size:22px;letter-spacing:1px;color:#c9a84c;margin-top:18px;}`,
  body:`<div class="wrap"><div class="h1">Know who to call.<br>Before they call<br><em>someone else</em>.</div>
    <div class="sub">StrategyAI · EMEIA mandate intelligence</div>
    <div class="url">${URL}</div></div>`});

let combinedPages = "";
slides.forEach((s, i) => {
  const html = slide(s, i + 1, s.swipe);
  fs.writeFileSync(path.join(OUT, s.id + ".html"), html);
  const inner = html.replace(/^[\s\S]*?<body>/, "").replace(/<\/body>[\s\S]*$/, "");
  combinedPages += `<div class="page">${inner}</div>`;
});

const combined = `<!doctype html><html><head><meta charset="utf-8"><style>${baseCss}
@page{size:1080px 1350px;margin:0;}
html,body{margin:0;padding:0;background:#0d1b2a;}
.page{width:1080px;height:1350px;overflow:hidden;page-break-after:always;break-after:page;}
.page:last-child{page-break-after:auto;break-after:auto;}
${slides.map(s=>s.css||"").join("\n")}
</style></head><body>${combinedPages}</body></html>`;
fs.writeFileSync(path.join(OUT, "_all.html"), combined);

console.log("wrote " + slides.length + " slide html + _all.html to " + OUT);
