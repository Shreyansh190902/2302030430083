// Renders every .slide in template.html to a 1080x1350 PNG (Instagram 4:5).
// Usage: node render.js
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  await page.goto('file://' + path.join(__dirname, 'template.html'));
  await page.evaluate(() => document.fonts.ready);
  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const out = path.join(__dirname, `slide-${i + 1}.png`);
    await slides[i].screenshot({ path: out });
    console.log('saved', out);
  }
  await browser.close();
})();
