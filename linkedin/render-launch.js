/* Render the newsletter launch graphic in dark + light. CI only. */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
(async () => {
  const outDir = path.resolve("launch/png");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 1800, deviceScaleFactor: 2 });
  await page.goto("file://" + path.resolve("launch/launch.html"), { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 900));
  for (const [id, name] of [["heroDark", "newsletter-launch-dark"], ["heroLight", "newsletter-launch-light"]]) {
    const el = await page.$("#" + id);
    await el.screenshot({ path: path.join(outDir, name + ".png") });
    console.log("rendered " + name + ".png");
  }
  // transparent device duo (laptop + phone) for the editable PowerPoint
  const dev = await page.$("#heroDark .stage");
  await dev.screenshot({ path: path.join(outDir, "newsletter-devices.png"), omitBackground: true });
  console.log("rendered newsletter-devices.png");
  await browser.close();
})();
