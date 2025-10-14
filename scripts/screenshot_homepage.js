const fs = require('fs');
const path = require('path');

(async () => {
  const url = process.env.SITE_URL || process.argv[2];
  const outPath = process.env.OUT_PATH || path.join('.github', 'preview.png');
  const width = parseInt(process.env.VIEWPORT_WIDTH || '1440', 10);
  const height = parseInt(process.env.VIEWPORT_HEIGHT || '900', 10);

  if (!url) {
    console.error('Missing SITE_URL. Provide env SITE_URL or first argument.');
    process.exit(1);
  }

  const puppeteer = require('puppeteer');
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width, height },
  });
  try {
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(60000);
    await page.goto(url, { waitUntil: 'networkidle2' });
    // Optional small delay for client-side hydration/animations
    await new Promise((r) => setTimeout(r, 1000));
    await fs.promises.mkdir(path.dirname(outPath), { recursive: true });
    await page.screenshot({ path: outPath, fullPage: false, type: 'png' });
    console.log('Saved screenshot to', outPath);
  } finally {
    await browser.close();
  }
})();
