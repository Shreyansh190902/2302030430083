// Renders each .slide in slides.html to out/NN.png (1080x1440).
// Usage: NODE_PATH=$(npm root -g) node render.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const out = path.join(__dirname, 'out');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });

  await page.goto('file://' + path.join(__dirname, 'slides.html'), { waitUntil: 'networkidle' });
  await page.evaluate(async () => { await Promise.all([...document.fonts].map(f => f.load().catch(() => {}))); });
  await page.evaluate(() => document.fonts.ready);
  for (const el of await page.$$('.slide')) {
    const id = (await el.getAttribute('id')).replace('s', '').padStart(2, '0');
    await el.screenshot({ path: path.join(out, `${id}.png`) });
  }
  await browser.close();
  console.log('rendered', fs.readdirSync(out).join(' '));
})();
