const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const C=fs.readFileSync(__dirname+'/c_ig.html','utf8');
const jobs=[['ep01-try-again','clean_f_26.5.png',1210,170,'I DID IT!','never give up'],
 ['ep02-colour-hunt','clean_e2.png',1060,160,'COLOUR<br>HUNT!','can you find red?'],
 ['ep04-copy-me','clean_e4.png',1190,180,'COPY ME!','can you jump?'],
 ['ep05-whats-missing','clean_e5.png',1060,150,'WHAT’S<br>MISSING?','can you remember?'],
 ['ep06-chuku-bridge','clean_e6.png',1060,150,'I GOT<br>AN IDEA!','stop, think, try!']];
for(const [n,img,top,sz,l1,l2] of jobs){fs.writeFileSync(__dirname+'/t.html',C.replace('__IMG__',img).replace('__TOP__',top).replace('__SIZE__',sz).replace('__L1__',l1).replace('__L2__',l2));
 await p.goto('file://'+__dirname+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:process.argv[2]+'/'+n+'-cover.png'})}
await b.close()})();
