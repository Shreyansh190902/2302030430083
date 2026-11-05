const { chromium } = require('playwright');
const path=require('path'), fs=require('fs');
const D=__dirname, OUT=process.argv[2];
const items=[
 ['dhanteras','शुभ धनतेरस','HAPPY DHANTERAS','May this Dhanteras bring good health, wealth and happiness to your home.'],
 ['diwali','शुभ दीपावली','HAPPY DIWALI','May the festival of lights fill your home with joy, love and togetherness.'],
 ['new-year','नूतन वर्षाभिनंदन','HAPPY NEW YEAR · SAAL MUBARAK','Wishing you a new year full of fresh beginnings and happy moments.'],
 ['bhai-dooj','भाई दूज की शुभकामनाएँ','HAPPY BHAI DOOJ','Celebrating the beautiful bond between brothers and sisters.'],
];
const html=(h,[k,hi,en,line])=>`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Yatra;src:url(yatra-one-devanagari-400-normal.woff2)}
@font-face{font-family:Mont;font-weight:500;src:url(montserrat-latin-500-normal.woff)}
@font-face{font-family:Mont;font-weight:600;src:url(montserrat-latin-600-normal.woff)}
@font-face{font-family:Mont;font-weight:700;src:url(montserrat-latin-700-normal.woff)}
body{margin:0;width:1080px;height:${h}px;background:url(bg_${h==1350?'feed':'story'}.png);position:relative;overflow:hidden}
.wrap{position:absolute;left:90px;right:90px;top:${h==1350?(hi.length>14?290:325):(hi.length>14?560:620)}px;text-align:center;color:#FCEBD2}
.logo{width:230px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35))}
.hi{font-family:Yatra;font-size:${hi.length>14?104:132}px;line-height:1.25;margin-top:${h==1350?40:70}px;
 background:linear-gradient(180deg,#FFF1B8 0%,#F5C95C 45%,#D99A2B 100%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(0 4px 10px rgba(60,0,0,.55))}
.rule{width:120px;height:2px;margin:26px auto 22px;background:linear-gradient(90deg,transparent,#F5C95C,transparent)}
.en{font-family:Mont;font-weight:700;font-size:30px;letter-spacing:6px;color:#F5C95C}
.line{font-family:Mont;font-weight:500;font-size:31px;line-height:1.5;margin:30px auto 0;max-width:800px}
.sig{font-family:Mont;font-weight:600;font-size:26px;letter-spacing:2px;margin-top:${h==1350?34:60}px;color:#F5C95C}
</style></head><body><div class="wrap"><img class="logo" src="logo.png"><div class="hi">${hi}</div><div class="rule"></div>
<div class="en">${en}</div><div class="line">${line}</div><div class="sig">— With warm wishes, Wudly Toys</div></div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const it of items)for(const h of [1350,1920]){fs.writeFileSync(path.join(D,'t.html'),html(h,it));
 await p.setViewportSize({width:1080,height:h});await p.goto('file://'+path.join(D,'t.html'));await p.waitForTimeout(400);
 await p.screenshot({path:path.join(OUT,`wudly-${it[0]}-${h==1350?'post':'story'}.png`)});}
await b.close();})();
