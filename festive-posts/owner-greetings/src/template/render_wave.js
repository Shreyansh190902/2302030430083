const { chromium } = require('playwright');
const path=require('path'), fs=require('fs');
const D=__dirname, OUT=process.argv[2];
const items=[
 ['dhanteras','शुभ धनतेरस','HAPPY DHANTERAS','May this Dhanteras bring good health, wealth and happiness to your home.'],
 ['diwali','शुभ दीपावली','HAPPY DIWALI','May the festival of lights fill your home with joy, love and togetherness.'],
 ['new-year','नूतन वर्षाभिनंदन',(process.argv[3]=='wave'?'HAPPY NEW YEAR':'HAPPY NEW YEAR · SAAL MUBARAK'),'Wishing you a new year full of fresh beginnings and happy moments.'],
 ['bhai-dooj','भाई दूज की शुभकामनाएँ','HAPPY BHAI DOOJ','Celebrating the beautiful bond between brothers and sisters.'],
];
const html=(h,[k,hi,en,line])=>`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Yatra;src:url(yatra-one-devanagari-400-normal.woff2)}
@font-face{font-family:Mont;font-weight:500;src:url(montserrat-latin-500-normal.woff)}
@font-face{font-family:Mont;font-weight:600;src:url(montserrat-latin-600-normal.woff)}
@font-face{font-family:Mont;font-weight:700;src:url(montserrat-latin-700-normal.woff)}
body{margin:0;width:1080px;height:${h}px;background:url(bgw_${h==1350?"feed":"story"}.png);overflow:hidden;display:flex;align-items:center;justify-content:center}
.wrap{width:640px;text-align:center;color:#3A2420;margin-top:${h==1350?0:80}px}
.logo{width:220px}
.hi{font-family:Yatra;font-size:${hi.length>14?100:104}px;line-height:1.25;margin-top:${h==1350?40:70}px;
 color:#8C1A08;
 }
.rule{width:120px;height:2px;margin:26px auto 22px;background:linear-gradient(90deg,transparent,#D9962B,transparent)}
.en{font-family:Mont;font-weight:700;font-size:30px;letter-spacing:4px;color:#C07A12}
.line{font-family:Mont;font-weight:500;font-size:29px;line-height:1.5;margin:26px auto 0;max-width:600px}
.sig{font-family:Mont;font-weight:600;font-size:26px;letter-spacing:2px;margin-top:${h==1350?34:60}px;color:#8C1A08}
</style></head><body><div class="wrap"><img class="logo" src="logo_red.png"><div class="hi">${hi}</div><div class="rule"></div>
<div class="en">${en}</div><div class="line">${line}</div><div class="sig">— With warm wishes, Wudly Toys</div></div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const it of items)for(const h of [1350,1920]){fs.writeFileSync(path.join(D,'t.html'),html(h,it));
 await p.setViewportSize({width:1080,height:h});await p.goto('file://'+path.join(D,'t.html'));await p.waitForTimeout(400);
 await p.screenshot({path:path.join(OUT,`wudly-${it[0]}-${h==1350?"post":"story"}.png`)});}
await b.close();})();
