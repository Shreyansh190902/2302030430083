const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const C=fs.readFileSync(__dirname+'/c.html','utf8');
const jobs=[['A',C.replace('__IMG__','clean_f_26.5.png').replace('__TOP__','1290').replace('__SIZE__','170').replace('__L1__','I DID IT!').replace('__L2__','never give up')],
            ['B',C.replace('__IMG__','clean_f_5.5.png').replace('__TOP__','1210').replace('__SIZE__','140').replace('__L1__','OH NO!<br>IT FELL…').replace('__L2__','again?!')]];
for(const [n,h] of jobs){fs.writeFileSync(__dirname+'/t.html',h);await p.goto('file://'+__dirname+'/t.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:process.argv[2]+'/thumb-'+n+'.png'})}
await p.goto('file://'+__dirname+'/r.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:process.argv[2]+'/thumb-C.png'});
await b.close()})();
