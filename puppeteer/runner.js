// runner.js — minimal Puppeteer test runner used by the tester agent.
//
// Usage:
//   node runner.js tests/<file>.test.js
//
// Each test file exports an async `run({ browser, page, helpers })`. The
// runner counts passes/fails and writes a JSON report to stdout that the
// orchestrator parses.

const path = require('path');
const fs = require('fs');

async function main() {
  const target = process.argv[2];
  if (!target) {
    console.error('usage: node runner.js <test-file-or-dir>');
    process.exit(2);
  }

  let puppeteer;
  try {
    puppeteer = require('puppeteer');
  } catch (e) {
    console.error('puppeteer not installed — run `npm install` in puppeteer/');
    process.exit(2);
  }

  const helpers = require('./helpers');
  const files = collectTestFiles(target);
  const results = { passed: 0, failed: 0, tests: [] };

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  for (const file of files) {
    const t0 = Date.now();
    const page = await browser.newPage();
    const mod = require(path.resolve(file));
    try {
      await mod.run({ browser, page, helpers });
      results.passed += 1;
      results.tests.push({ file, status: 'pass', ms: Date.now() - t0 });
    } catch (err) {
      results.failed += 1;
      results.tests.push({
        file,
        status: 'fail',
        ms: Date.now() - t0,
        error: err.message,
      });
    } finally {
      await page.close();
    }
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 2));
  process.exit(results.failed > 0 ? 1 : 0);
}

function collectTestFiles(target) {
  const stat = fs.statSync(target);
  if (stat.isFile()) return [target];
  return fs
    .readdirSync(target)
    .filter((f) => f.endsWith('.test.js'))
    .map((f) => path.join(target, f));
}

main().catch((e) => {
  console.error(e);
  process.exit(2);
});
