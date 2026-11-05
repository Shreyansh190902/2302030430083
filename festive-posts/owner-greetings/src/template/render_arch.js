const {chromium}=require('playwright');const path=require('path'),fs=require('fs');const D=__dirname;
// key, small word, big word, line, area per size {h:[top,bottom]}
const items=[
 ['dhanteras','शुभ','धनतेरस','Wishing you good health, wealth and happiness this Dhanteras.',{1350:[150,700],1920:[300,1180]}],
 ['diwali','शुभ','दीपावली','Wishing you peace, prosperity and a joyful Diwali celebration.',{1350:[110,820],1920:[400,1180]}],
 ['new-year','नूतन','वर्षाभिनंदन','Wishing you a new year full of fresh beginnings and happy moments.',{1350:[230,960],1920:[480,1200]}],
 ['bhai-dooj','शुभ','भाई दूज','Celebrating the beautiful bond between brothers and sisters.',{1350:[150,880],1920:[300,1200]}],
];
const only=process.argv[3]?process.argv[3].split(','):null; const H=parseInt(process.argv[4]||'1350');
const html=([k,sm,big,line,area],h)=>`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Amita;font-weight:700;src:url(amita-devanagari-700-normal.woff2)}
@font-face{font-family:Mont;font-weight:400;src:url(montserrat-latin-400-normal.woff)}
@font-face{font-family:Mont;font-weight:500;src:url(montserrat-latin-500-normal.woff)}
body{margin:0;width:1080px;height:${h}px;background:url(arch_${k}_${h==1350?'feed':'story'}.png);background-size:cover;overflow:hidden;position:relative}
.area{position:absolute;left:0;right:0;top:${area[h][0]}px;height:${area[h][1]-area[h][0]}px;display:flex;align-items:center;justify-content:center}
.wrap{width:540px;text-align:center;color:#fff}
.sm{font-family:Amita;font-weight:700;font-size:64px;line-height:1;color:#F9A825;margin:0 0 6px 110px;text-shadow:0 2px 6px rgba(60,0,10,.35)}
.big{display:inline-block;font-family:Amita;font-weight:700;font-size:150px;line-height:1.25;white-space:nowrap;text-shadow:0 3px 10px rgba(60,0,10,.4)}
.line{font-family:Mont;font-weight:400;font-size:28px;line-height:1.5;margin-top:18px}
.logo{width:150px;margin-top:30px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.25))}
</style></head><body><div class="area"><div class="wrap"><div class="sm">${sm}</div><div class="big" id="big">${big}</div>
<div class="line">${line}</div><img class="logo" src="logo.png"></div></div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:H}});
for(const it of items){if(only&&!only.includes(it[0]))continue;fs.writeFileSync(path.join(D,'t.html'),html(it,H));
 await p.goto('file://'+path.join(D,'t.html'));
 const MW=H==1920?{'dhanteras':600,'diwali':560,'new-year':560,'bhai-dooj':600}[it[0]]:{'dhanteras':560,'diwali':480,'new-year':460,'bhai-dooj':540}[it[0]];await p.evaluate(async(MW)=>{await document.fonts.ready;const e=document.getElementById('big');let s=150;while(e.getBoundingClientRect().width>MW&&s>70){s-=4;e.style.fontSize=s+'px'}},MW);await p.waitForTimeout(200);
 await p.screenshot({path:path.join(process.argv[2],`wudly-${it[0]}-${H==1350?'post':'story'}.png`)});}
await b.close();})();
