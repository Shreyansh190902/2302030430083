const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2160,height:3840}});
await p.goto('file://'+__dirname+'/outro.html');await p.waitForTimeout(500);
const seek=t=>p.evaluate(t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})},t);
const list=process.argv[3]?process.argv[3].split(',').map(Number):[...Array(138).keys()];
for(const f of list){await seek(f*1000/30);await p.screenshot({path:`${process.argv[2]}/n${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});}
await b.close()})();
