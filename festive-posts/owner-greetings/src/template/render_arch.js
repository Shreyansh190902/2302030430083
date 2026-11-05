const {chromium}=require('playwright');const path=require('path'),fs=require('fs');const D=__dirname;
// key, small word, big word, line, area per size {h:[top,bottom]}
const items=[
 ['dhanteras','शुभ','धनतेरस','Wishing you good health, wealth and happiness.',{1350:[150,700],1920:[300,1180]}],
 ['diwali','शुभ','दीपावली','Wishing you peace, prosperity and joy.',{1350:[110,820],1920:[400,1180]}],
 ['new-year','नूतन','वर्षाभिनंदन','Wishing you a year of fresh beginnings.',{1350:[230,960],1920:[480,1200]}],
 ['bhai-dooj','शुभ','भाई दूज','Celebrating the bond of brothers and sisters.',{1350:[150,880],1920:[300,1200]}],
];
const BANDS=JSON.parse(fs.readFileSync(path.join(D,'arch_bands.json')));
const LAYER=process.env.LAYER||'';const TXT=!!LAYER;
const only=process.argv[3]?process.argv[3].split(','):null; const H=parseInt(process.argv[4]||'1350');

const petals=(r,n,len,w)=>{let o='';for(let i=0;i<n;i++){const a=360*i/n;o+=`<ellipse cx="0" cy="${-r}" rx="${w}" ry="${len}" transform="rotate(${a})" fill="none" stroke="#F5C95C" stroke-width="2"/>`}return o};
const dots=(r,n,d)=>{let o='';for(let i=0;i<n;i++){const a=2*Math.PI*i/n;o+=`<circle cx="${(r*Math.cos(a)).toFixed(1)}" cy="${(r*Math.sin(a)).toFixed(1)}" r="${d}" fill="#F5C95C"/>`}return o};
const MANDALA=(sz)=>`<svg class="mandala" width="${sz}" height="${sz}" viewBox="-300 -300 600 600">
<circle r="290" fill="none" stroke="#F5C95C" stroke-width="2"/><circle r="270" fill="none" stroke="#F5C95C" stroke-width="1" stroke-dasharray="4 8"/>
${petals(225,24,48,16)}${dots(170,48,3)}${petals(130,16,38,14)}<circle r="85" fill="none" stroke="#F5C95C" stroke-width="2"/>${petals(55,12,22,9)}${dots(282,72,2.5)}</svg>`;
const STAR=(x,y,z)=>`<svg class="spark" style="left:${x}px;top:${y}px;width:${z}px;height:${z}px" viewBox="-10 -10 20 20"><path d="M0-10 2-2 10 0 2 2 0 10-2 2-10 0-2-2Z"/></svg>`;
const DIYA=`<svg width="34" height="26" viewBox="0 0 34 26"><path d="M17 1c3 4 4 7 0 10-4-3-3-6 0-10z" fill="#F9C74F"/><path d="M2 13h30c-2 7-8 11-15 11S4 20 2 13z" fill="#F5C95C"/></svg>`;
const html=([k,sm,big,line,area],h)=>`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Amita;font-weight:700;src:url(amita-devanagari-700-normal.woff2)}
@font-face{font-family:Mont;font-weight:400;src:url(montserrat-latin-400-normal.woff)}
@font-face{font-family:Mont;font-weight:500;src:url(montserrat-latin-500-normal.woff)}
body{margin:0;width:1080px;height:${h}px;${TXT?'background:transparent;':`background:url(arch_${k}_${h==1350?'feed':'story'}.png);background-size:cover;`}overflow:hidden;position:relative}
.area{position:absolute;left:0;right:0;top:${BANDS[k][h][0]}px;height:${BANDS[k][h][1]-BANDS[k][h][0]}px;display:flex;align-items:center;justify-content:center}
.wrap{width:520px;transform-origin:center center;text-align:center;color:#fff}
.sm{font-family:Amita;font-weight:700;font-size:64px;line-height:1;color:#F9A825;margin:0 0 4px 0;text-shadow:0 2px 6px rgba(60,0,10,.35)}
.big{display:inline-block;font-family:Amita;font-weight:700;font-size:150px;line-height:1.25;white-space:nowrap;text-shadow:0 3px 10px rgba(60,0,10,.4)}
.line{text-wrap:balance;font-family:Mont;font-weight:400;font-size:27px;line-height:1.45;margin-top:10px}
.mandala{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);opacity:.32;pointer-events:none}
.spark{position:absolute;fill:#F9C74F;filter:drop-shadow(0 0 6px rgba(255,200,80,.9))}
.div{display:flex;align-items:center;justify-content:center;gap:12px;margin:16px auto 4px}
.div i{display:block;height:2px;width:90px;background:linear-gradient(90deg,transparent,#F5C95C)}
.div i:last-child{background:linear-gradient(90deg,#F5C95C,transparent)}
.logo{width:150px;margin-top:20px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.25))}
${LAYER=='deco'?'.wrap{visibility:hidden}':''}${LAYER=='text'?'.mandala,.spark{display:none}':''}</style></head><body><div class="area">${MANDALA(Math.min(760,(BANDS[k][h][1]-BANDS[k][h][0])+120))}<div class="wrap"><div class="sm">${sm}</div><div class="big" id="big">${big}</div>
<div class="div"><i></i>${DIYA}<i></i></div><div class="line">${line}</div><img class="logo" src="logo.png"></div></div>${(()=>{const [t,b]=BANDS[k][h];const pts=[[300,t+30,26],[760,t+70,20],[330,b-60,18],[740,b-40,28],[270,(t+b)/2,14],[800,(t+b)/2+30,16]];return pts.map(([x,y,z])=>STAR(x,y,z)).join("")})()}</body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:H}});
for(const it of items){if(only&&!only.includes(it[0]))continue;fs.writeFileSync(path.join(D,'t.html'),html(it,H));
 await p.goto('file://'+path.join(D,'t.html'));
 const MW=450;const CAPV={'dhanteras':640,'diwali':560,'new-year':520,'bhai-dooj':640}[it[0]];await p.evaluate(async([MW,CAP])=>{await document.fonts.ready;const e=document.getElementById('big');let s=150;while(e.getBoundingClientRect().width>MW&&s>70){s-=4;e.style.fontSize=s+'px'}
 const w=document.querySelector('.wrap'),ar=document.querySelector('.area');const cap=innerHeight>1500?CAP/520:1;const sc=Math.min(cap,(ar.clientHeight*0.95)/w.scrollHeight);w.style.transform='scale('+sc+')';},[MW,CAPV]);await p.waitForTimeout(200);
 await p.screenshot({omitBackground:TXT,path:path.join(process.argv[2],`wudly-${it[0]}-${H==1350?'post':'story'}${TXT?'-layer-'+LAYER:''}.png`)});}
await b.close();})();
