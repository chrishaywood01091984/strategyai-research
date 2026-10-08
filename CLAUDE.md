# strategyai-research: read before adding or editing an article

This repo is the live research site (research.strategyai.co.uk). Pushing main publishes immediately: get Chris's OK.

Design: the master brand system is `strategyai-brain/assets/brand/BRAND.md` (8 Oct 2026). Articles use the
"2026-10 THEME" block at the end of `assets/style.css`: white page, navy data panels, Gloock headlines, Hanken
Grotesk body, lavender `#C9B6F2` highlights in charts, purple `#7A5CA8` links. No cream, no gold, no Fraunces /
Playfair / Inter / Mono fonts.

New article: copy `business-services/index.html` (same head: embed script, the website redirect, the Gloock + Hanken
font link, `/assets/style.css?v=9`; bump the version whenever style.css changes). Then add it to `ARTICLES` in
`strategyai/src/pages/Research.jsx` so it appears on strategyai.co.uk/research.
