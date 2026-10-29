# Three quieter ascents, with the original portrait

The user selected High Pass but found the animations too loud and literal. This review removes the cycling graphics, reduces the ascent motif, explores a small Sisyphus reference, and restores the existing portrait in three different placements.

| Option | Portrait | Main cue | Floating header |
| --- | --- | --- | --- |
| [A measured ascent](quiet-incline/index.html) | Small portrait beside the introductory heading | Two spare ridge lines and a single point | Tiny ascending steps and a point |
| [The quiet push](quiet-sisyphus/index.html) | Portrait anchoring the personal sidebar | A very small Sisyphus figure and stone | Stone and incline only |
| [The cairn](quiet-cairn/index.html) | Larger portrait where the main illustration previously sat | A ridgeline and small cairn beneath the portrait | Three stacked stones |

Open [quiet.html](quiet.html) for the full-page captures, header details, and optional live previews.

## Photo

The image is `img/kakto.jpg`, the existing `_config.yml` profile photo. It was visually inspected before use. The original file, colors, and identity are retained. Sizing and framing use ordinary HTML/CSS; the photo is not replaced, generated, or retouched. All new pages link to the actual existing asset through `../../img/kakto.jpg`.

The other local portraits were not substituted. This keeps the exact image currently associated with the public site in the review. The chosen placement can later be used on the final homepage and About page.

## Restraint

The main cue travels at most 16 SVG units (roughly 14 screen pixels at desktop), and the header cue at most 12 SVG units (roughly 6 screen pixels). There are no pedaling limbs, moving scenery, route reveals, bounces, or automatic resets. The small stone rotates only 32 degrees over the corresponding scroll range. Scrolling backward reverses the change.

The cairn changes emphasis rather than position: all stones are present from the beginning, with a restrained opacity change. The main scene responds while the introduction is visible; the smaller cue follows overall reading progress after the introduction leaves. Native scrolling is unchanged. Reduced motion freezes the main illustration and hides the extra header cue; JavaScript off leaves a static illustration and the original photo.

Sisyphus appears as a small effort/persistence motif, not a cartoon sequence or a quotation attributed to a philosopher. The metaphor introduces no new factual claims about Mario's professional or sporting history.

The large agent panel remains removed. **Agent version** remains a quiet top-level link, and all real writing and history pages remain linked. Core introduction, article text, and sidebar descriptions are unchanged from High Pass, apart from the added portrait/name caption.

## Source and checks

- Original photo: `img/kakto.jpg` from the repository root, or `../img/kakto.jpg` from this document.
- New SVGs: `art/quiet-*-main.svg`, `art/quiet-*-header.svg`.
- Style/motion: `assets/quiet.css`, `assets/quiet.js`.
- Variants and shared template: `../scripts/render-designs.rb`, `templates/page.erb`.
- Render with `./scripts/render-designs` from the repository root.
- Optional browser check/capture: `scripts/capture-quiet.py` in the documented Playwright environment, while serving the repo at port 4173.
- Captures: `assets/quiet-*-desktop.png`, phone and header captures, and `assets/quiet-comparison.png`.

Browser checks verify photo identity/loading, source content, quiet agent navigation, bounded motion, scroll reversal, idle state, header spacing at phone/tablet widths, reduced motion, no-JavaScript reading, real article bodies, and live previews. The shared checker also validates all review HTML file links and viewport overflow. Full Safari/Firefox and screen-reader review remain later validation tasks.

These files are design-review artifacts, excluded from Jekyll production output. No deployment is implied.
