const {chromium}=require('playwright');const path=require('path'),fs=require('fs');const D=__dirname;
const items=[
 ['dhanteras','शुभ धनतेरस','Happy Dhanteras','May this Dhanteras bring good health, wealth and happiness to your home.'],
 ['diwali','शुभ दीपावली','Happy Diwali','May the festival of lights fill your home with joy, love and togetherness.'],
 ['new-year','नूतन वर्षाभिनंदन','Happy New Year','Wishing you a new year full of fresh beginnings and happy moments.'],
 ['bhai-dooj','भाई दूज की शुभकामनाएँ','Happy Bhai Dooj','Celebrating the beautiful bond between brothers and sisters.'],
];
const GOLD={hi:'linear-gradient(180deg,#FFF1B8 0%,#F5C95C 45%,#D99A2B 100%)',en:'#F5C95C',line:'#FCEBD2',sig:'#F5C95C',logo:'logo.png',shadow:'drop-shadow(0 4px 10px rgba(60,0,0,.55))'};
const MAROON={hi:'#8C1A08',en:'#B5701A',line:'#3A2420',sig:'#8C1A08',logo:'logo_red.png',shadow:'none'};
const SETS={
 'fireworks':{bg:'bg',c:GOLD,area:{1350:[290,1080],1920:[380,1620]},w:{1350:880,1920:880},out:'.'},
 'corner-frame':{bg:'bgc',c:GOLD,area:{1350:[170,1180],1920:[230,1690]},w:{1350:860,1920:860},out:'corner-frame'},
 'wave-frame':{bg:'bgw',c:MAROON,area:{1350:[150,1200],1920:[380,1700]},w:{1350:560,1920:560},out:'wave-frame'},
 'diya-maroon':{bg:'bgd',c:GOLD,area:{1350:[400,1150],1920:[960,1760]},w:{1350:640,1920:700},out:'diya-maroon'},
};
const html=(S,h,[k,hi,en,line])=>{const c=S.c,[a,b]=S.area[h],w=S.w[h],long=hi.includes('शुभकामनाएँ');return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Amita;font-weight:700;src:url(amita-devanagari-700-normal.woff2)}
@font-face{font-family:PF;font-style:italic;font-weight:600;src:url(playfair-display-latin-600-italic.woff2)}
@font-face{font-family:Mar;src:url(marcellus-latin-400-normal.woff2)}
@font-face{font-family:Cor;font-style:italic;font-weight:500;src:url(cormorant-garamond-latin-500-italic.woff2)}
body{margin:0;width:1080px;height:${h}px;background:url(${S.bg}_${h==1350?'feed':'story'}.png);overflow:hidden;position:relative}
.area{position:absolute;left:0;right:0;top:${a}px;height:${b-a}px;display:flex;align-items:center;justify-content:center}
.wrap{width:${w}px;text-align:center}
.logo{width:${w<700?200:230}px;filter:${c.shadow=='none'?'none':'drop-shadow(0 6px 14px rgba(0,0,0,.35))'}}
.hi{font-family:Amita;font-weight:700;font-size:${long?(w<700?92:104):(w<700?112:136)}px;line-height:${long?1.45:1.3};margin-top:22px;${long?'':'white-space:nowrap;'}
 ${c.hi.startsWith('linear')?`background:${c.hi};-webkit-background-clip:text;color:transparent;`:`color:${c.hi};`}filter:${c.shadow}}
.en{font-family:PF;font-style:italic;font-weight:600;font-size:${w<700?50:58}px;color:${c.en};margin-top:4px}
.rule{width:140px;height:2px;margin:22px auto 20px;background:linear-gradient(90deg,transparent,${c.en},transparent)}
.line{max-width:${Math.min(w,740)}px;margin:0 auto;font-family:Cor;font-style:italic;font-weight:500;font-size:${w<700?36:40}px;line-height:1.35;color:${c.line}}
.sig{font-family:Mar;font-size:24px;letter-spacing:3px;margin-top:26px;color:${c.sig}}
</style></head><body><div class="area"><div class="wrap"><img class="logo" src="${c.logo}"><div class="hi" id="hi">${hi}</div>
<div class="en">${en}</div><div class="rule"></div><div class="line">${line}</div><div class="sig">WITH WARM WISHES, WUDLY TOYS</div></div></div>
</body></html>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [name,S] of Object.entries(SETS)){const out=path.join(process.argv[2],S.out);
 for(const it of items)for(const h of [1350,1920]){fs.writeFileSync(path.join(D,'t.html'),html(S,h,it));
  await p.setViewportSize({width:1080,height:h});await p.goto('file://'+path.join(D,'t.html'));await p.evaluate(async()=>{await document.fonts.ready;const e=document.getElementById('hi');let s=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>e.clientWidth+2&&s>50){s-=2;e.style.fontSize=s+'px'}});await p.waitForTimeout(200);
  await p.screenshot({path:path.join(out,`wudly-${it[0]}-${h==1350?'post':'story'}.png`)});}}
await b.close();})();
