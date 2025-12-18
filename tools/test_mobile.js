/**
 * Mobile viewport test - takes screenshot at mobile resolution
 * Run: node tools/test_mobile.js
 */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const HTML_PATH = path.resolve(__dirname, '../brand-kit/digital/business-card.html');

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Set mobile viewport (iPhone 12 Pro)
  await page.setViewport({
    width: 390,
    height: 844,
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true
  });

  console.log('Loading page...');
  await page.goto(`file://${HTML_PATH}`, { waitUntil: 'networkidle0' });

  // Wait for styles to apply
  await new Promise(r => setTimeout(r, 500));

  // Check what's visible
  const visibility = await page.evaluate(() => {
    const browser = document.querySelector('.left .browser');
    const hero = document.querySelector('.left .mobile-hero');
    
    const browserStyle = browser ? getComputedStyle(browser) : null;
    const heroStyle = hero ? getComputedStyle(hero) : null;
    
    return {
      browserDisplay: browserStyle?.display,
      heroDisplay: heroStyle?.display,
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
      matchesMedia720: window.matchMedia('(max-width: 720px)').matches,
      matchesMedia900: window.matchMedia('(max-width: 900px)').matches
    };
  });

  console.log('\n=== VISIBILITY CHECK ===');
  console.log(`Viewport: ${visibility.viewportWidth}x${visibility.viewportHeight}`);
  console.log(`Media (max-width: 720px): ${visibility.matchesMedia720}`);
  console.log(`Media (max-width: 900px): ${visibility.matchesMedia900}`);
  console.log(`Browser display: ${visibility.browserDisplay}`);
  console.log(`Mobile-hero display: ${visibility.heroDisplay}`);

  // Take screenshot
  const screenshotPath = path.resolve(__dirname, 'mobile_test_screenshot.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`\nScreenshot saved: ${screenshotPath}`);

  // Also test landscape
  await page.setViewport({
    width: 844,
    height: 390,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true
  });
  await new Promise(r => setTimeout(r, 300));

  const landscapeVisibility = await page.evaluate(() => {
    const browser = document.querySelector('.left .browser');
    const hero = document.querySelector('.left .mobile-hero');
    
    const browserStyle = browser ? getComputedStyle(browser) : null;
    const heroStyle = hero ? getComputedStyle(hero) : null;
    
    return {
      browserDisplay: browserStyle?.display,
      heroDisplay: heroStyle?.display,
      viewportWidth: window.innerWidth,
      matchesMedia900Landscape: window.matchMedia('(max-width: 900px) and (orientation: landscape)').matches
    };
  });

  console.log('\n=== LANDSCAPE CHECK ===');
  console.log(`Viewport: ${landscapeVisibility.viewportWidth}px wide`);
  console.log(`Media (max-width: 900px, landscape): ${landscapeVisibility.matchesMedia900Landscape}`);
  console.log(`Browser display: ${landscapeVisibility.browserDisplay}`);
  console.log(`Mobile-hero display: ${landscapeVisibility.heroDisplay}`);

  const landscapePath = path.resolve(__dirname, 'mobile_test_landscape.png');
  await page.screenshot({ path: landscapePath, fullPage: false });
  console.log(`Landscape screenshot: ${landscapePath}`);

  await browser.close();
  
  // Summary
  console.log('\n=== SUMMARY ===');
  if (visibility.browserDisplay === 'none' && visibility.heroDisplay !== 'none') {
    console.log('✅ PORTRAIT: Browser hidden, hero visible - CORRECT');
  } else {
    console.log(`❌ PORTRAIT: Browser=${visibility.browserDisplay}, Hero=${visibility.heroDisplay} - INCORRECT`);
  }
  
  if (landscapeVisibility.browserDisplay === 'none' && landscapeVisibility.heroDisplay !== 'none') {
    console.log('✅ LANDSCAPE: Browser hidden, hero visible - CORRECT');
  } else {
    console.log(`❌ LANDSCAPE: Browser=${landscapeVisibility.browserDisplay}, Hero=${landscapeVisibility.heroDisplay} - INCORRECT`);
  }
})();
