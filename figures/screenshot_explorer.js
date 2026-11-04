// Screenshot the bia_curriculum explorer for slide 14.
//
//   git clone https://github.com/acorbat/bia_curriculum && cd bia_curriculum
//   python scripts/build_curriculum.py && python -m http.server 8765 --directory web &
//   node <this repo>/figures/screenshot_explorer.js        # needs: npm i playwright
//
// Optional: CYTOSCAPE=/path/to/cytoscape.min.js serves a local copy instead of the CDN.
// Then run figures/make_figures.py, which crops explorer_psf.png -> explorer_psf_crop.png.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, 'out');
const BASE = process.env.EXPLORER_URL || 'http://127.0.0.1:8765/';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  if (process.env.CYTOSCAPE) {
    await page.route('**/cytoscape.min.js', r =>
      r.fulfill({ body: fs.readFileSync(process.env.CYTOSCAPE), contentType: 'application/javascript' }));
  }
  const shots = [
    ['', 'explorer_all'],
    ['?path=PATH-bia-for-biologists', 'explorer_biologists'],
    ['?path=PATH-bia-for-biologists&topic=TOP-psf-and-resolution', 'explorer_psf'],
  ];
  for (const [query, name] of shots) {
    await page.goto(BASE + query);
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  }
  await browser.close();
})();
