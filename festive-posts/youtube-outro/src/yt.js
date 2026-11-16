const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+__dirname+'/yt.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
const seek=t=>p.evaluate(t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})},t);
const list=process.argv[3]?process.argv[3].split(',').map(Number):[...Array(600).keys()];
for(const f of list){await seek(f*1000/30);await p.screenshot({path:`${process.argv[2]}/y${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});}
await b.close()})();
