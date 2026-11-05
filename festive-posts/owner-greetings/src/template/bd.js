const {chromium}=require('playwright');const fs=require('fs');const D=__dirname;
const OUT=process.argv[2], MODE=process.argv[3]||'still';
const CFG={story:{h:1920,bg:'bd_story.png',t:250,a:820,s:.8,flames:[],kids:[[330,1180],[700,1120]]},
           post:{h:1350,bg:'bd_feed.png',t:150,a:560,s:.6,flames:[],kids:[[480,880],[760,860]]}};
const rnd=i=>{let x=Math.sin(i*99.13)*43758.5;return x-Math.floor(x)};
const fx=c=>c.flames.map(([x,y,r])=>`<div class="glow" style="left:${x}px;top:${y}px;width:${r}px;height:${r*1.4}px"></div>`).join('')
 +Array.from({length:24},(_,i)=>`<div class="sp" style="left:${(80+rnd(i+7)*920).toFixed(0)}px;top:${(c.h*0.5+rnd(i+31)*c.h*0.45).toFixed(0)}px;animation-duration:${(4+rnd(i+3)*3).toFixed(2)}s;animation-delay:-${(rnd(i+11)*6).toFixed(2)}s"></div>`).join('')
 +c.kids.flatMap(([x,y],k)=>[0,1].map(j=>`<div class="heart" style="left:${x+j*40-20}px;top:${y}px;animation-delay:${(4.6+k*.9+j*1.7).toFixed(1)}s">♥</div>`)).join('');
(async()=>{const b=await chromium.launch();
for(const [name,c] of Object.entries(CFG)){
 fs.writeFileSync(D+'/t_bd.html',fs.readFileSync(D+'/bd.html','utf8').replace('__H__',c.h).replace('__BG__',c.bg).replace('__T__',c.t).replace('__A__',c.a).replace('__S__',c.s).replace('__FX__',fx(c)));
 const p=await b.newPage({viewport:{width:1080,height:c.h}});await p.goto('file://'+D+'/t_bd.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 const seek=async t=>p.evaluate(t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})},t);
 if(MODE==='still'){await seek(7600);await p.evaluate(()=>document.querySelectorAll('.heart').forEach(h=>h.style.display='none'));await p.screenshot({path:`${OUT}/wudly-bhai-dooj-ramayan-${name}.png`});}
 else if(name===MODE){fs.mkdirSync(OUT,{recursive:true});for(let f=0;f<240;f++){await seek(f*1000/30);await p.screenshot({path:`${OUT}/f${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}}
 await p.close()}
await b.close()})();
