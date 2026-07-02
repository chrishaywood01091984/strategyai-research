/* Render a week's slide HTML into PNGs + a combined PDF, using puppeteer (headless Chrome).
 * Usage: node render.js <htmlDir> [pdfName]
 *   e.g. node render.js week01/html StrategyAI_Week1_carousel.pdf
 * Outputs: <weekDir>/png/*.png and <weekDir>/<pdfName>
 * Runs in CI (GitHub Actions) so no rendering happens on any local machine.
 */
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

(async () => {
  const htmlDir = path.resolve(process.argv[2] || "week01/html");
  const pdfName = process.argv[3] || "StrategyAI_Week1_carousel.pdf";
  const weekDir = path.dirname(htmlDir);
  const pngDir = path.join(weekDir, "png");
  fs.mkdirSync(pngDir, { recursive: true });

  const slides = fs.readdirSync(htmlDir).filter(f => /^\d.*\.html$/.test(f)).sort();
  const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-gpu"] });

  for (const f of slides) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
    await page.goto("file://" + path.join(htmlDir, f), { waitUntil: "networkidle0" });
    try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
    await page.screenshot({ path: path.join(pngDir, f.replace(".html", ".png")) });
    await page.close();
    console.log("png " + f.replace(".html", ".png"));
  }

  const all = path.join(htmlDir, "_all.html");
  if (fs.existsSync(all)) {
    const page = await browser.newPage();
    await page.goto("file://" + all, { waitUntil: "networkidle0" });
    try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
    await new Promise(r => setTimeout(r, 500));
    await page.pdf({
      path: path.join(weekDir, pdfName),
      width: "1080px", height: "1350px",
      printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });
    await page.close();
    console.log("pdf " + pdfName);
  }

  await browser.close();
})();
