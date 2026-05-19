// helpers/index.js — small, single-purpose helpers for Puppeteer tests.

module.exports = {
  async waitForText(page, text, timeout = 5000) {
    await page.waitForFunction(
      (t) => document.body && document.body.innerText.includes(t),
      { timeout },
      text,
    );
  },

  async fillField(page, selector, value) {
    await page.waitForSelector(selector);
    await page.click(selector, { clickCount: 3 });
    await page.type(selector, value);
  },

  async clickAndWait(page, selector, nav = false) {
    await page.waitForSelector(selector);
    if (nav) {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
        page.click(selector),
      ]);
    } else {
      await page.click(selector);
    }
  },

  assert(cond, msg) {
    if (!cond) throw new Error(`assertion failed: ${msg}`);
  },
};
