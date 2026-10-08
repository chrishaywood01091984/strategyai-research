/* StrategyAI Research — data-driven SVG charts (brand-styled, no deps).
   Usage:
   <div data-area='{"values":[...],"labels":[...],"peak":"text"}'></div>
   <div data-bars='{"rows":[{"label":"x","value":10,"gold":true}],"unit":"deals"}'></div> */
(function(){
  function area(d){
    const v=d.values, lab=d.labels, n=v.length;
    const x0=58,x1=662,y0=30,y1=250, plotW=x1-x0;
    const yMax=Math.max(...v)*1.14||1;
    const X=i=> x0 + i*(plotW/(n-1));
    const Y=val=> y1 - (val/yMax)*(y1-y0);
    let grid='',ylab='';
    for(let f=0;f<=1.001;f+=0.25){const gy=y1-f*(y1-y0);
      grid+=`<line x1="${x0}" y1="${gy.toFixed(1)}" x2="${x1}" y2="${gy.toFixed(1)}"/>`;
      ylab+=`<text x="${x0-10}" y="${(gy+4).toFixed(1)}">${Math.round(f*yMax)}</text>`;}
    let pts=v.map((val,i)=>`${X(i).toFixed(1)},${Y(val).toFixed(1)}`).join(' ');
    let areaPath=`M${x0},${y1} L`+pts.replace(/ /g,' L')+` L${x1},${y1} Z`;
    let dots=v.map((val,i)=>`<circle cx="${X(i).toFixed(1)}" cy="${Y(val).toFixed(1)}" r="${i===n-1?5:3.2}"/>`).join('');
    let xlab=lab.map((l,i)=>`<text x="${X(i).toFixed(1)}" y="272" text-anchor="middle">${l}</text>`).join('');
    let peak = d.peak? `<line x1="${X(n-1).toFixed(1)}" y1="${(Y(v[n-1])+8).toFixed(1)}" x2="${X(n-1).toFixed(1)}" y2="${y1}" stroke="#C9B6F2" stroke-opacity=".35" stroke-dasharray="3 4"/><text x="${(X(n-1)-8).toFixed(1)}" y="${Math.max(Y(v[n-1])-12,22).toFixed(1)}" text-anchor="end" fill="#C9B6F2" font-family="Gloock,serif" font-style="italic" font-size="15">${d.peak}</text>`:'';
    return `<svg viewBox="0 0 720 300" role="img" aria-label="trend chart">
      <defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9B6F2" stop-opacity=".42"/><stop offset="1" stop-color="#C9B6F2" stop-opacity="0"/></linearGradient></defs>
      <g stroke="#8FA3BD" stroke-opacity=".18">${grid}</g>
      <g fill="#8FA3BD" font-family="Hanken Grotesk,sans-serif" font-size="11" text-anchor="end">${ylab}</g>
      <path d="${areaPath}" fill="url(#ga)"/>
      <polyline points="${pts}" fill="none" stroke="#C9B6F2" stroke-width="2.6" stroke-linejoin="round"/>
      <g fill="#C9B6F2">${dots}</g>${peak}
      <g fill="#8FA3BD" font-family="Hanken Grotesk,sans-serif" font-size="11">${xlab}</g></svg>`;
  }
  function bars(d){
    const rows=d.rows, n=rows.length, max=Math.max(...rows.map(r=>r.value))||1;
    const x0=210,x1=610,bw=x1-x0, top=24, step=Math.min(46,(276)/n), h=Math.min(26,step-16);
    let out='';
    rows.forEach((r,i)=>{const y=top+i*step; const w=(r.value/max)*bw;
      out+=`<text x="${x0-15}" y="${y+h/2+5}" text-anchor="end" fill="#8FA3BD" font-family="Hanken Grotesk,sans-serif" font-size="12">${r.label}</text>`;
      out+=`<rect x="${x0}" y="${y}" width="${w.toFixed(1)}" height="${h}" rx="3" fill="${r.gold?'#C9B6F2':'#4d7fa0'}"/>`;
      out+=`<text x="${(x0+w+8).toFixed(1)}" y="${y+h/2+5}" fill="${r.gold?'#fff':'#dce4ee'}" font-family="Hanken Grotesk,sans-serif" font-size="12">${r.value}${d.unit?(' '+d.unit):''}</text>`;});
    const vb=`0 0 720 ${top+n*step+6}`;
    return `<svg viewBox="${vb}" role="img" aria-label="bar chart"><g>${out}</g></svg>`;
  }
  // Donut with a legend: {"rows":[{"label":"Strategic","value":68}],"centre":"96","sub":"deals"}
  function donut(d){
    const pal=['#C9B6F2','#7FB0E0','#3CCB95','#4d7fa0','#9FB0C4','#7A4FA0','#E39B7B','#5E7389'];
    const rows=d.rows, tot=rows.reduce((a,r)=>a+r.value,0)||1, cx=130, cy=130, R=104, r=66;
    let a0=-Math.PI/2, segs='', leg='';
    rows.forEach((row,i)=>{
      const frac=row.value/tot, a1=a0+frac*Math.PI*2, big=frac>0.5?1:0, col=pal[i%pal.length];
      const p=(ang,rad)=>[(cx+rad*Math.cos(ang)).toFixed(2),(cy+rad*Math.sin(ang)).toFixed(2)];
      if(frac>=0.9999){segs+='<circle cx="'+cx+'" cy="'+cy+'" r="'+((R+r)/2)+'" fill="none" stroke="'+col+'" stroke-width="'+(R-r)+'"/>';}
      else{const [x1,y1]=p(a0,R),[x2,y2]=p(a1,R),[x3,y3]=p(a1,r),[x4,y4]=p(a0,r);
        segs+='<path d="M'+x1+' '+y1+' A'+R+' '+R+' 0 '+big+' 1 '+x2+' '+y2+' L'+x3+' '+y3+' A'+r+' '+r+' 0 '+big+' 0 '+x4+' '+y4+' Z" fill="'+col+'" stroke="#0F1B2D" stroke-width="2"/>';}
      const ly=40+i*30;
      leg+='<rect x="290" y="'+(ly-10)+'" width="12" height="12" rx="3" fill="'+col+'"/>'
        +'<text x="312" y="'+ly+'" fill="#DCE4EE" font-family="Hanken Grotesk,sans-serif" font-size="14">'+row.label+'</text>'
        +'<text x="690" y="'+ly+'" text-anchor="end" fill="#fff" font-family="Hanken Grotesk,sans-serif" font-size="14" font-weight="700">'+Math.round(frac*100)+'%</text>'
        +'<text x="640" y="'+ly+'" text-anchor="end" fill="#8FA3BD" font-family="Hanken Grotesk,sans-serif" font-size="13">'+row.value+'</text>';
      a0=a1;});
    const h=Math.max(260,40+rows.length*30);
    return '<svg viewBox="0 0 720 '+h+'" role="img" aria-label="share chart">'+segs
      +'<text x="'+cx+'" y="'+(cy+6)+'" text-anchor="middle" fill="#fff" font-family="Gloock,serif" font-size="38">'+(d.centre||tot)+'</text>'
      +'<text x="'+cx+'" y="'+(cy+30)+'" text-anchor="middle" fill="#8FA3BD" font-family="Hanken Grotesk,sans-serif" font-size="12" letter-spacing="2">'+(d.sub||'').toUpperCase()+'</text>'
      +leg+'</svg>';
  }
  function render(){
    document.querySelectorAll('[data-area]').forEach(el=>{try{el.innerHTML=area(JSON.parse(el.dataset.area))}catch(e){}});
    document.querySelectorAll('[data-donut]').forEach(el=>{try{el.innerHTML=donut(JSON.parse(el.dataset.donut))}catch(e){}});
    document.querySelectorAll('[data-bars]').forEach(el=>{try{el.innerHTML=bars(JSON.parse(el.dataset.bars))}catch(e){}});
  }
  if(document.readyState!=='loading') render(); else document.addEventListener('DOMContentLoaded',render);
})();
