/* StrategyAI Research — shared front-end logic.
   Supabase is wired but optional: the UI degrades gracefully until keys/tables are live. */
const SUPA = {
  url: window.SUPA_URL || "",         // set at deploy: https://gvdfeqzhizlzpybdibca.supabase.co
  anonKey: window.SUPA_ANON || ""      // public anon/publishable key
};

/* ---------- node-graph hero canvas (brand motif) ---------- */
function nodeField(canvas){
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  let w,h,pts;
  function size(){
    w = canvas.width = canvas.offsetWidth * devicePixelRatio;
    h = canvas.height = canvas.offsetHeight * devicePixelRatio;
    const n = Math.min(70, Math.floor(w*h/26000));
    pts = Array.from({length:n},()=>({
      x:Math.random()*w, y:Math.random()*h,
      vx:(Math.random()-.5)*.12*devicePixelRatio, vy:(Math.random()-.5)*.12*devicePixelRatio,
      r:(Math.random()*1.6+0.6)*devicePixelRatio
    }));
  }
  function draw(){
    ctx.clearRect(0,0,w,h);
    for(let i=0;i<pts.length;i++){
      const a=pts[i]; a.x+=a.vx; a.y+=a.vy;
      if(a.x<0||a.x>w)a.vx*=-1; if(a.y<0||a.y>h)a.vy*=-1;
      for(let j=i+1;j<pts.length;j++){
        const b=pts[j], d=Math.hypot(a.x-b.x,a.y-b.y);
        if(d<150*devicePixelRatio){
          ctx.strokeStyle=`rgba(143,163,189,${(1-d/(150*devicePixelRatio))*.16})`;
          ctx.lineWidth=devicePixelRatio*.6;
          ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
        }
      }
    }
    for(const p of pts){
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,7);
      ctx.fillStyle = p.r>1.6*devicePixelRatio ? 'rgba(201,168,76,.7)' : 'rgba(110,190,210,.55)';
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  size(); draw(); addEventListener('resize',size);
}

/* ---------- filters (hub) ---------- */
function initFilters(){
  const chips=document.querySelectorAll('.chip'); if(!chips.length) return;
  chips.forEach(c=>c.addEventListener('click',()=>{
    chips.forEach(x=>x.classList.remove('active')); c.classList.add('active');
    const f=c.dataset.filter;
    document.querySelectorAll('[data-cat]').forEach(card=>{
      card.style.display = (f==='all'||card.dataset.cat===f) ? '' : 'none';
    });
  }));
}

/* ---------- likes (Supabase RPC + localStorage de-dupe) ---------- */
async function initLikes(){
  const btns=document.querySelectorAll('.like-btn,[data-like]'); if(!btns.length) return;
  const liked=JSON.parse(localStorage.getItem('sa_liked')||'{}');
  btns.forEach(btn=>{
    const slug=btn.dataset.slug; if(!slug) return;
    if(liked[slug]) btn.classList.add('liked');
    btn.addEventListener('click',async()=>{
      if(liked[slug]) return;
      liked[slug]=1; localStorage.setItem('sa_liked',JSON.stringify(liked));
      btn.classList.add('liked');
      const c=btn.querySelector('.count'); if(c) c.textContent=(+c.textContent+1);
      try{ if(SUPA.url) await fetch(`${SUPA.url}/rest/v1/rpc/increment_like`,{
        method:'POST',headers:{'apikey':SUPA.anonKey,'Content-Type':'application/json'},
        body:JSON.stringify({post_slug:slug})});}catch(e){}
    });
  });
}

/* ---------- share ---------- */
function initShare(){
  const _c=document.querySelector('link[rel="canonical"]');
  const canon=(_c&&_c.href)||location.href.split('?')[0];
  const url=encodeURIComponent(canon);
  const title=encodeURIComponent(document.title);
  document.querySelectorAll('[data-share]').forEach(a=>{
    const k=a.dataset.share;
    if(k==='linkedin') a.href='https://www.linkedin.com/company/strategyaiintelligenceuk/';
    if(k==='x') a.href=`https://twitter.com/intent/tweet?url=${url}&text=${title}`;
    if(k!=='copy') a.target='_blank';
    if(k==='copy') a.addEventListener('click',e=>{e.preventDefault();
      navigator.clipboard.writeText(canon);a.title='Link copied';});
  });
}

function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

/* ---------- community posts (approved, contributor) ---------- */
async function loadCommunity(){
  const grid=document.getElementById('community-grid'); if(!grid||!SUPA.url) return;
  try{
    const r=await fetch(`${SUPA.url}/rest/v1/research_posts?status=eq.approved&is_staff=eq.false&order=published_at.desc&select=slug,title,excerpt,category,likes,author_name`,{headers:{apikey:SUPA.anonKey}});
    const posts=await r.json();
    if(!Array.isArray(posts)||!posts.length) return;
    grid.innerHTML = posts.map(p=>`
      <a class="card" data-cat="community" target="_top" href="https://research.strategyai.co.uk/post?slug=${encodeURIComponent(p.slug)}">
        <div class="thumb"><span class="cat">Community</span></div>
        <div class="body"><h3>${esc(p.title)}</h3><p>${esc(p.excerpt||'')}</p>
          <div class="meta"><span>${esc(p.author_name||'Contributor')}</span><span class="like">&#9829; ${p.likes||0}</span></div></div>
      </a>`).join('');
  }catch(e){}
}

/* ---------- mobile nav toggle (injected on every page) ---------- */
function navToggle(){
  const wrap=document.querySelector('.nav .wrap');
  const links=wrap&&wrap.querySelector('.navlinks');
  if(!wrap||!links||wrap.querySelector('.nav-toggle')) return;
  const b=document.createElement('button');
  b.className='nav-toggle'; b.setAttribute('aria-label','Menu'); b.setAttribute('aria-expanded','false');
  b.innerHTML='&#9776;';
  b.addEventListener('click',()=>{const o=links.classList.toggle('open');b.setAttribute('aria-expanded',o);b.innerHTML=o?'&#10005;':'&#9776;';});
  links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{links.classList.remove('open');b.innerHTML='&#9776;';}));
  wrap.appendChild(b);
}

/* ---------- wide article layout: main column + sticky rail (2026-10 theme) ---------- */
const PIECES=[
  ['european-deal-monitor',"Europe's dealmaking quarter",'Market Insight'],['deal-report','The 30-Day Deal Report','Report'],
  ['healthcare-mandates-forming','Healthcare M&A: where the next mandates are forming','Market Insight'],['tmt',"TMT: the integration wave",'Sector read'],
  ['fig','FIG: the +92% quarter','Sector read'],['business-services','Business Services: 83% carry an integration mandate','Sector read'],
  ['energy-infrastructure','Energy & Infrastructure: capital deploys, the work forms','Sector read'],['industrials','Industrials: big-ticket integration','Sector read'],
  ['materials-chemicals',"Materials & Chemicals: the +164% quarter",'Sector read'],['consumer-retail','Consumer & Retail: the sector that cooled','Sector read'],
  ['private-equity','Private Equity: every deal is a mandate','Sector read'],['market-outlook','Where the market is heading','Outlook']];
function articleLayout(){
  const art=document.querySelector('article.article'); const by=art&&art.querySelector('.byline');
  if(!art||!by||art.querySelector('.a-body')) return;
  const body=document.createElement('div'); body.className='a-body';
  const main=document.createElement('div'); main.className='a-main';
  let n=by.nextElementSibling; while(n){const nx=n.nextElementSibling; main.appendChild(n); n=nx;}
  const slug=location.pathname.split('/').filter(Boolean)[0]||'';
  const hs=[...main.querySelectorAll(':scope > h2, .upd > h2')].filter(h=>!h.closest('.cta-band'));
  hs.forEach((h,i)=>{if(!h.id)h.id='s'+(i+1);});
  const more=PIECES.filter(p=>p[0]!==slug).slice(0,4);
  const rail=document.createElement('aside'); rail.className='a-rail';
  rail.innerHTML=(hs.length?'<div class="rb toc-box"><div class="rl">In this piece</div><nav class="toc">'+hs.map(h=>'<a href="#'+h.id+'" data-id="'+h.id+'">'+esc(h.textContent)+'</a>').join('')+'</nav></div>':'')
    +'<div class="rb rcta"><div class="rl">◆ StrategyAI</div><p>The mandates forming in your sectors, ranked, with the evidence, the people and the route in.</p><p>One mandate pays for it many times over. <a href="https://strategyai.co.uk/client-access#the-maths" target="_top" style="display:inline;padding:0;background:none;color:#C9B6F2;font:inherit;letter-spacing:0;text-transform:none;text-decoration:none;font-weight:600">Run the maths ›</a></p><a href="https://strategyai.co.uk/client-access" target="_top">Get access</a></div>'
    +'<div class="rb more"><div class="rl">More research</div>'+more.map(p=>'<a href="https://strategyai.co.uk/research/'+p[0]+'" target="_top"><b>'+esc(p[1])+'</b><span>'+esc(p[2])+'</span></a>').join('')+'</div>';
  body.appendChild(main); body.appendChild(rail); art.appendChild(body);
  rail.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();const t=document.getElementById(a.dataset.id);if(t)t.scrollIntoView({behavior:'smooth',block:'start'});}));
  const links=[...rail.querySelectorAll('.toc a')];
  const pick=()=>{let cur=hs[0]&&hs[0].id;hs.forEach(h=>{if(h.getBoundingClientRect().top<160)cur=h.id;});links.forEach(l=>l.classList.toggle('on',l.dataset.id===cur));};
  pick(); addEventListener('scroll',pick,{passive:true});
}

document.addEventListener('DOMContentLoaded',()=>{
  articleLayout();
  nodeField(document.getElementById('nodefield'));
  navToggle(); initFilters(); initLikes(); initShare(); loadCommunity();
});

/* ---------- report content height to Base44 parent (auto-resize embed) ---------- */
(function(){
  if(window.parent===window) return;            // only when embedded in an iframe
  var last=0;
  function H(){ return Math.max(document.body?document.body.scrollHeight:0, document.documentElement.scrollHeight, document.documentElement.offsetHeight); }
  function post(force){ var h=Math.ceil(H()); if(force||Math.abs(h-last)>2){ last=h; try{ parent.postMessage({type:'sa-research-height', height:h}, '*'); }catch(e){} } }
  addEventListener('DOMContentLoaded', function(){post(1)});
  addEventListener('load', function(){post(1)});
  addEventListener('resize', function(){post(1)});
  if(document.images) for(var i=0;i<document.images.length;i++){ document.images[i].addEventListener('load', function(){post(1)}); }
  var n=0, iv=setInterval(function(){ post(); if(++n>25) clearInterval(iv); }, 350);   // ~9s safety net
  try{ new ResizeObserver(function(){post()}).observe(document.documentElement); }catch(e){}
  try{ new MutationObserver(function(){post()}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,characterData:true}); }catch(e){}
  post(1);
})();
