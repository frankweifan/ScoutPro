// Rasterise Tabler icons (from icons.json) to PNG in given colours: node icons_png.js outdir hex1 hex2 ...
const sharp = require('sharp'); const fs = require('fs'); const path = require('path');
const icons = JSON.parse(fs.readFileSync(path.join(__dirname, 'icons.json')));
const out = process.argv[2]; const cols = process.argv.slice(3);
fs.mkdirSync(out, { recursive: true });
(async () => {
  for (const [n, svg] of Object.entries(icons)) for (const c of cols) {
    const s = svg.replace('stroke="currentColor"', `stroke="#${c}"`).replace('height="24" width="24"', 'height="256" width="256"');
    await sharp(Buffer.from(s)).png().toFile(path.join(out, `${n}_${c}.png`));
  }
})();
