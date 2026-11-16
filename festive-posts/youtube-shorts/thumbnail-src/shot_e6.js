const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const h=fs.readFileSync(__dirname+'/c.html','utf8').replace('__IMG__','clean_e6.png').replace('__TOP__','1280').replace('__SIZE__','160').replace('__L1__','I GOT<br>AN IDEA!').replace('__L2__','stop, think, try!');
fs.writeFileSync(__dirname+'/t.html',h);await p.goto('file://'+__dirname+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:process.argv[2]});await b.close()})();
