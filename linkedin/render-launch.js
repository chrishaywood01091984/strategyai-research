/* Render the newsletter launch graphic (laptop + phone overlap + copy). CI only. */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
(async () => {
  const outDir = path.resolve("launch/png");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 2 });
  await page.goto("file://" + path.resolve("launch/launch.html"), { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 800));
  const el = await page.$(".hero");
  await el.screenshot({ path: path.join(outDir, "newsletter-launch.png") });
  console.log("rendered launch/png/newsletter-launch.png");
  await browser.close();
})();
