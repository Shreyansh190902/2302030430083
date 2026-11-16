const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const h=fs.readFileSync(__dirname+'/c.html','utf8').replace('__IMG__','clean_e2.png').replace('__TOP__','1170').replace('__SIZE__','170').replace('__L1__','COLOUR<br>HUNT!').replace('__L2__','can you find red?');
fs.writeFileSync(__dirname+'/t.html',h);await p.goto('file://'+__dirname+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:process.argv[2]});await b.close()})();
