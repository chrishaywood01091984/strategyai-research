/* Render the LinkedIn company banner HTML into a PNG using puppeteer (headless Chrome).
 * Runs in CI (GitHub Actions) only - no rendering on any local machine.
 * Output: banner/png/li-company-banner.png  (1128x191 @ 3x = 3384x573)
 */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

(async () => {
  const outDir = path.resolve("banner/png");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1128, height: 191, deviceScaleFactor: 3 });
  await page.goto("file://" + path.resolve("banner/banner.html"), { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(outDir, "li-company-banner.png") });
  console.log("rendered banner/png/li-company-banner.png");
  await page.close();
  await browser.close();
})();
