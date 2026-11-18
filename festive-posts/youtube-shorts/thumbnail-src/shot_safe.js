const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const C=fs.readFileSync(__dirname+'/c_safe.html','utf8');const out=process.argv[2];
const J=[
['ep001-thumbnail-i-did-it','clean_f_26.5.png',170,'I DID IT!','never give up'],
['ep002-thumbnail-colour-hunt','clean_e2.png',170,'COLOUR<br>HUNT!','can you find red?'],
['ep004-thumbnail-copy-me','clean_e4.png',190,'COPY ME!','can you jump?'],
['ep005-thumbnail-whats-missing','clean_e5.png',160,'WHAT’S<br>MISSING?','can you remember?'],
['ep006-thumbnail-chuku-bridge','clean_e6.png',160,'I GOT<br>AN IDEA!','stop, think, try!'],
['ep007-thumbnail-rainy-day-blocks','clean_e7.png',170,'WOBBLE…<br>TUMBLE!','3 rainy-day games'],
['ep010-thumbnail-magic-seed','clean_e10.png',170,'IT GREW<br>SO BIG!','be patient!'],
['ep011-thumbnail-paper-plane','clean_e11.png',170,'TRY<br>AGAIN!','it flies!'],
['ep012-thumbnail-bubble-trouble','clean_e12.png',170,'AS BIG<br>AS ME!','giant bubble!'],
['ep013-thumbnail-puddle-splash','clean_e13.png',170,'1, 2, 3…<br>SPLASH!','puddle time!'],
['ep014-thumbnail-kite-wind','clean_e14.png',170,'UP, UP,<br>UP!','keep trying!']];
for(const [n,img,sz,l1,l2] of J){fs.writeFileSync(__dirname+'/t.html',C.replace('__IMG__',img).replace('__SIZE__',sz).replace('__L1__',l1).replace('__L2__',l2));
await p.goto('file://'+__dirname+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:out+'/'+n+'.png'})}
await b.close()})();
