// Renders every .slide in an HTML template to 1080x1350 PNGs (Instagram 4:5).
// Usage: node render.js [template.html] [output-prefix]
//   node render.js                      -> slide-1.png ...
//   node render.js minimal.html minimal -> minimal-1.png ...
const path = require('path');
const { chromium } = require('playwright');

const file = process.argv[2] || 'template.html';
const prefix = process.argv[3] || 'slide';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  await page.goto('file://' + path.resolve(__dirname, file));
  await page.evaluate(() => document.fonts.ready);
  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const out = path.join(__dirname, `${prefix}-${i + 1}.png`);
    await slides[i].screenshot({ path: out });
    console.log('saved', out);
  }
  await browser.close();
})();
