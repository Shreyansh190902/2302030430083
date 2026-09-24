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

  // Slide 01 is the provided cover, resized to 1080x1440.
  await page.setContent(`<body style="margin:0"><img id="c" src="file://${path.join(__dirname, 'assets/cover.webp')}" style="width:1080px;height:1440px;display:block"></body>`);
  await page.waitForFunction(() => document.getElementById('c').complete);
  await (await page.$('#c')).screenshot({ path: path.join(out, '01.png') });

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
