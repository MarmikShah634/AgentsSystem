// example.test.js — reference Puppeteer test exercising the helper API.
// Replace the URL/assertions when wiring to a real app.

module.exports = {
  async run({ page, helpers }) {
    await page.goto('https://example.com/', { waitUntil: 'domcontentloaded' });
    const title = await page.title();
    helpers.assert(title.includes('Example'), `unexpected title: ${title}`);
    await helpers.waitForText(page, 'Example Domain');
  },
};
