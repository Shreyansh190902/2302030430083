const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const D=__dirname;
const OUT=process.argv[2], MODE=process.argv[3]||'still';
const CFG={
 story:{h:1920,bg:'ny_story.png',t:560,a:520,s:.78,flames:[[534,329,150],[187,1546,150],[868,1417,190]],bulbs:[[60,140],[150,120],[245,100],[330,80],[415,62],[500,52],[585,50],[670,58],[755,72],[840,92],[925,115],[1010,135]]},
 post:{h:1350,bg:'ny_feed.png',t:440,a:380,s:.6,flames:[[597,257,130],[247,1195,130],[630,1182,200]],bulbs:[[40,60],[160,48],[280,40],[400,34],[520,30],[640,32],[760,38],[880,46],[1000,58]]}};
const rnd=(i)=>{let x=Math.sin(i*99.13)*43758.5;return x-Math.floor(x)};
const fx=c=>c.flames.map(([x,y,r],i)=>`<div class="glow" style="left:${x}px;top:${y}px;width:${r}px;height:${r*1.4}px;animation-delay:-${(i*.37).toFixed(2)}s;animation-duration:${(1.1+i*.23).toFixed(2)}s"></div>`).join('')
 +c.bulbs.map(([x,y],i)=>`<div class="tw" style="left:${x}px;top:${y}px;animation-delay:-${(rnd(i)*1.6).toFixed(2)}s"></div>`).join('')
 +Array.from({length:26},(_,i)=>`<div class="sp" style="left:${(80+rnd(i+7)*920).toFixed(0)}px;top:${(c.h*0.55+rnd(i+31)*c.h*0.4).toFixed(0)}px;animation-duration:${(4+rnd(i+3)*3).toFixed(2)}s;animation-delay:-${(rnd(i+11)*6).toFixed(2)}s;transform:scale(${(.5+rnd(i+5)).toFixed(2)})"></div>`).join('');
(async()=>{const b=await chromium.launch();
for(const [name,c] of Object.entries(CFG)){
 const html=fs.readFileSync(D+'/ny.html','utf8').replace('__H__',c.h).replace('__BG__',c.bg).replace('__T__',c.t).replace('__A__',c.a).replace('__S__',c.s).replace('__FX__',fx(c));
 fs.writeFileSync(D+'/t_ny.html',html);
 const p=await b.newPage({viewport:{width:1080,height:c.h}});await p.goto('file://'+D+'/t_ny.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 const seek=async t=>p.evaluate(t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})},t);
 if(MODE==='still'){await seek(7600);await p.screenshot({path:`${OUT}/wudly-new-year-red-${name}.png`});}
 else if(name===MODE){const dir=OUT;fs.mkdirSync(dir,{recursive:true});const N=8*30;
  for(let f=0;f<N;f++){await seek(f*1000/30);await p.screenshot({path:`${dir}/f${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}}
 await p.close()}
await b.close()})();
