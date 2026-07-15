/* Render 300x300 newsletter cover options to PNGs (3x for crispness). CI only. */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

(async () => {
  const outDir = path.resolve("covers/png");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 700, deviceScaleFactor: 3 });
  await page.goto("file://" + path.resolve("covers/covers.html"), { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await new Promise(r => setTimeout(r, 700));
  for (const id of ["c1", "c2", "c3"]) {
    const el = await page.$("#" + id);
    await el.screenshot({ path: path.join(outDir, `newsletter-cover-${id}.png`) });
    console.log("rendered newsletter-cover-" + id + ".png");
  }
  await browser.close();
})();
