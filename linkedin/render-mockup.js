/* Render the "In your pocket" mobile mockup scene to a PNG for LinkedIn.
 * Runs in CI (GitHub Actions) only - no rendering on any local machine.
 * Output: mockup/png/strategyai-mobile-mockup.png (2x scale).
 */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

(async () => {
  const outDir = path.resolve("mockup/png");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1240, height: 900, deviceScaleFactor: 2 });
  await page.goto("file://" + path.resolve("mockup/mockup-scene.html"), { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 700));
  const el = await page.$(".sai-scene");
  await el.screenshot({ path: path.join(outDir, "strategyai-mobile-mockup.png") });
  console.log("rendered mockup/png/strategyai-mobile-mockup.png");
  await browser.close();
})();
