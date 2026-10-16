// Usage: node render.js page.html out.pdf [--png-dir dir] [--width-mm 297 --height-mm 210]
// Renders HTML to PDF with Chromium; optionally screenshots every [data-export] element to PNG.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const html = path.resolve(args[0]); const out = args[1];
  const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
  const pngDir = opt('--png-dir', null);
  const w = opt('--width-mm', '297'), h = opt('--height-mm', '210');
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.goto('file://' + html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  if (out && out !== '-') {
    await page.pdf({ path: out, width: w + 'mm', height: h + 'mm', printBackground: true, preferCSSPageSize: true });
  }
  if (pngDir) {
    const els = await page.$$('[data-export]');
    for (const el of els) {
      const name = await el.getAttribute('data-export');
      const scale = parseFloat((await el.getAttribute('data-scale')) || '1');
      const box = await el.boundingBox();
      const p2 = await browser.newPage({ deviceScaleFactor: 2 * scale, viewport: { width: Math.ceil(box.width), height: Math.ceil(box.height) } });
      const outer = await el.evaluate(e => e.outerHTML);
      const styles = await page.evaluate(() => [...document.querySelectorAll('style')].map(s => s.outerHTML).join(''));
      await p2.setContent(`<html><head>${styles}<style>html,body{margin:0;padding:0;background:transparent}</style></head><body>${outer}</body></html>`, { waitUntil: 'networkidle' });
      await p2.evaluate(() => document.fonts.ready);
      const el2 = await p2.$('[data-export]');
      await el2.screenshot({ path: path.join(pngDir, name + '.png'), omitBackground: true });
      await p2.close();
    }
  }
  await browser.close();
})();
