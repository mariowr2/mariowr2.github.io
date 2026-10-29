# Three low mountain marks on A Measured Ascent

The selected layout is A Measured Ascent, including the original portrait beside the introductory heading. The user wants to remove the ascent motif and replace the tall, attention-seeking mountain with three muted representations whose movement is visible before the graphic scrolls away.

## Options

- [Thin ridgeline](mountain-ridge/index.html): two spare, panoramic outlines, with a small separation between the near and far layers.
- [Contour band](mountain-contour/index.html): a narrow set of topographic curves, with a gentle horizontal shift between sets.
- [Layered horizon](mountain-horizon/index.html): two low, filled silhouettes with a restrained edge and small depth change.

Compare at [mountains.html](mountains.html). All use exactly the same portrait placement, copy, writing, sidebar, and quiet agent tab. The graphics contain no climber, Sisyphus figure, stone, route, or moving progress dot. Earlier options are preserved.

## The timing fix

The old main SVG occupied roughly 140–160px of height. The new strips are 52–56px high. They no longer add a large illustration row on a phone.

The main motion is driven by a short visible scroll window, not the entire introduction or document. On load, fonts-ready, and resize, the implementation measures the strip and masthead. It starts after the strip becomes fully visible on short screens, and completes within 48–96px of scrolling while the strip is still on screen. In normal desktop conditions it starts with the first scroll. The header handoff is based on the strip passing the sticky masthead, rather than waiting for the entire introductory section to disappear.

Near/far layers move at most a few SVG units, with a slight change in emphasis. The floating header uses a smaller version of the corresponding mark, driven by page reading progress. Scrolling back reverses both. There is no autoplay, loop, path tracing, cursor animation, or scroll interception.

Reduced motion freezes the main strip and hides the additional header mark. Without JavaScript, the low SVG and all normal content remain visible. Motion is scoped to homepages; full article/history views remain available as static pages.

## Source and reproduction

- SVGs: `art/mountain-*-main.svg`, `art/mountain-*-header.svg`.
- Style/motion: `assets/mountains.css`, `assets/mountains.js`.
- Shared template/renderer: `templates/page.erb`, `../scripts/render-designs.rb`.
- Regenerate with `./scripts/render-designs` from the repository root.
- Browser check/capture: `scripts/capture-mountains.py` in the documented Playwright environment, with the repo served at port 4173.
- Captures include marks at actual size, page/phone views, and the gallery under `assets/mountain-*.png` and `assets/mountains-comparison.png`.

Checks explicitly verify that progress changes while the strip is still visible above the masthead, rather than merely testing a changed SVG somewhere off screen. They also check the 56px height limit, unchanged selected content, original image, quiet agent link, scroll reversal/idle, phone/header layout, reduced motion, no-JavaScript, and live previews. The broader review checker covers all HTML links and viewport overflow.

These remain excluded design-review artifacts, not a deployed redesign.
