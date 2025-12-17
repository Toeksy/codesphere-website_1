/*
  UI smoke checks (Playwright) for Codesphere static site.
  Runs in a container (recommended) so results are consistent.

  What it verifies:
  - device-preview landscape iframe shows the business card (not blank)
  - index.html background canvas draws non-empty pixels ("starfield"/particles)
  - business-card desktop enables live preview iframe (same-origin)
*/

const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const ARTIFACTS_DIR = path.join(__dirname, 'ui-smoke-artifacts');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.html':
      return 'text/html; charset=utf-8';
    case '.css':
      return 'text/css; charset=utf-8';
    case '.js':
      return 'application/javascript; charset=utf-8';
    case '.json':
      return 'application/json; charset=utf-8';
    case '.svg':
      return 'image/svg+xml';
    case '.png':
      return 'image/png';
    case '.jpg':
    case '.jpeg':
      return 'image/jpeg';
    case '.ico':
      return 'image/x-icon';
    case '.vcf':
      return 'text/vcard; charset=utf-8';
    case '.pdf':
      return 'application/pdf';
    default:
      return 'application/octet-stream';
  }
}

function startStaticServer(rootDir, port = 4173) {
  const server = http.createServer((req, res) => {
    try {
      const url = new URL(req.url, `http://${req.headers.host}`);
      let pathname = decodeURIComponent(url.pathname);

      if (pathname === '/') pathname = '/index.html';

      // Prevent path traversal
      const safePath = path.normalize(pathname).replace(/^([\\/])+/, '');
      const filePath = path.join(rootDir, safePath);
      const resolved = path.resolve(filePath);
      if (!resolved.startsWith(path.resolve(rootDir) + path.sep)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
      }

      fs.readFile(resolved, (err, data) => {
        if (err) {
          res.writeHead(404);
          res.end('Not found');
          return;
        }
        res.writeHead(200, {
          'Content-Type': contentTypeFor(resolved),
          'Cache-Control': 'no-store',
        });
        res.end(data);
      });
    } catch (e) {
      res.writeHead(500);
      res.end('Server error');
    }
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(port, '0.0.0.0', () => {
      resolve({
        server,
        baseUrl: `http://127.0.0.1:${port}`,
      });
    });
  });
}

async function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function run() {
  ensureDir(ARTIFACTS_DIR);

  const { server, baseUrl } = await startStaticServer(ROOT, 4173);
  const browser = await chromium.launch();

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
  });

  const page = await context.newPage();

  try {
    // 1) device-preview landscape must show business card content
    {
      const url = `${baseUrl}/device-preview.html?v=smoke`;
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(300);

      // The landscape iframe is titled "Mobiili vaaka" in device-preview.html
      const landscapeFrame = page.frame({ name: null, url: /business-card\.html/i }) || null;
      // If multiple frames match, pick by iframe title.
      const landscapeHandle = await page.$('iframe[title="Mobiili vaaka"]');
      await assert(!!landscapeHandle, 'Missing landscape iframe (title="Mobiili vaaka")');

      const frame = await landscapeHandle.contentFrame();
      await assert(!!frame, 'Unable to access landscape iframe content frame');

      // Wait for card to render
      await frame.waitForSelector('.card', { timeout: 8000 });

      const hasBrand = await frame.locator('text=CODESPHERE').first().isVisible();
      await assert(hasBrand, 'Landscape card does not show CODESPHERE (possibly blank/collapsed)');

      // Measure inside the iframe coordinate space (not affected by parent scaling).
      const env = await frame.evaluate(() => ({
        innerWidth,
        innerHeight,
        orientationLandscape: window.matchMedia('(orientation: landscape)').matches,
        mqMaxW720: window.matchMedia('(max-width: 720px)').matches,
      }));

      await assert(
        env && env.orientationLandscape && env.innerWidth > env.innerHeight,
        `Landscape iframe is not landscape: ${JSON.stringify(env)}`
      );

      const cardRect = await frame.evaluate(() => {
        const el = document.querySelector('.card');
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return { width: r.width, height: r.height };
      });
      await assert(
        cardRect && cardRect.width > 300 && cardRect.height > 180,
        `Landscape card size too small in iframe coords: rect=${JSON.stringify(cardRect)} env=${JSON.stringify(env)}`
      );

      await page.screenshot({ path: path.join(ARTIFACTS_DIR, 'device-preview.png'), fullPage: true });
    }

    // 2) index.html background canvas draws pixels (starfield/particles)
    {
      const url = `${baseUrl}/index.html?v=smoke`;
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(800);

      const hasCanvas = await page.locator('#bg-canvas').count();
      await assert(hasCanvas === 1, 'Missing #bg-canvas');

      const nonEmpty = await page.evaluate(() => {
        const canvas = document.getElementById('bg-canvas');
        if (!canvas) return false;
        const ctx = canvas.getContext('2d');
        if (!ctx) return false;
        if (!canvas.width || !canvas.height) return false;

        const samples = [
          [0.5, 0.5],
          [0.25, 0.25],
          [0.75, 0.25],
          [0.25, 0.75],
          [0.75, 0.75],
          [0.5, 0.2],
          [0.5, 0.8],
        ];

        for (const [fx, fy] of samples) {
          const x = Math.floor(canvas.width * fx);
          const y = Math.floor(canvas.height * fy);
          const img = ctx.getImageData(Math.max(0, x - 40), Math.max(0, y - 40), 80, 80);
          for (let i = 3; i < img.data.length; i += 4) {
            if (img.data[i] !== 0) return true; // alpha > 0
          }
        }

        return false;
      });

      await assert(nonEmpty, 'Background canvas appears empty (no drawn pixels)');
      await page.screenshot({ path: path.join(ARTIFACTS_DIR, 'index.png'), fullPage: false });
    }

    // 3) business-card desktop enables live preview iframe
    {
      const url = `${baseUrl}/brand-kit/digital/business-card.html?v=smoke`;
      await page.setViewportSize({ width: 1200, height: 700 });
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(400);

      const isLive = await page.evaluate(() => {
        const preview = document.querySelector('.preview');
        return !!(preview && preview.classList.contains('is-live'));
      });
      await assert(isLive, 'Desktop business-card did not enable live preview (.preview.is-live)');

      const iframeSrc = await page.getAttribute('#sitePreview', 'src');
      await assert(iframeSrc && iframeSrc.includes('index.html'), `Live preview iframe missing/incorrect src: ${iframeSrc}`);

      const siteFrame = await (await page.$('#sitePreview')).contentFrame();
      await assert(!!siteFrame, 'Unable to access #sitePreview frame');
      await siteFrame.waitForTimeout(800);

      // Verify the site actually rendered inside the iframe.
      await assert((await siteFrame.locator('#bg-canvas').count()) === 1, 'Live preview iframe missing #bg-canvas');
      const navVisible = await siteFrame.locator('.nav').first().isVisible().catch(() => false);
      await assert(navVisible, 'Live preview iframe missing visible .nav');

      await page.screenshot({ path: path.join(ARTIFACTS_DIR, 'business-card-desktop.png'), fullPage: true });
    }

    console.log('UI SMOKE: PASS');
  } finally {
    await browser.close().catch(() => {});
    await new Promise((resolve) => server.close(resolve));
  }
}

run().catch((err) => {
  console.error('UI SMOKE: FAIL');
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
