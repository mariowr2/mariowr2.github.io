# Six main/header animation pairings

The user selected the Summit Companion and floating header, then requested a better main animation plus a distinct header animation. The agent section should become much quieter. Six complete alternatives extend Still Climbing without changing its introduction, posts, or professional history.

| Pair | Main illustration | Floating header |
| --- | --- | --- |
| [The ascent](pair-ridge/index.html) | Layered ridgelines, a winding route, a walking hiker, and a cairn | An overhead close-up of switchbacks with a marker |
| [High pass](pair-pass/index.html) | A bicycle climbing a winding road through a mountain pass | A side-on cyclist with turning wheels on a rolling road |
| [After dark](pair-night/index.html) | A headlamp climbing above a small camp in a night landscape | A resting cat that wakes, stretches, and moves its tail |
| [Contour study](pair-contour/index.html) | Original topographic contours and a route winding into their center | A runner advancing on a trail with a changing stride |
| [One more ridge](pair-traverse/index.html) | A hiker crossing a saddle before a further climb | A different elevation profile traced with reading progress |
| [The window seat](pair-window/index.html) | A cat watching mountains and a moving cyclist through a window | A separate walking cat with moving paws and tail |

Review [pairings.html](pairings.html). Each card shows an actual capture of the main artwork and its different header companion. Expand a live preview or open the full page to scroll it. Static gallery captures show representative states, not the whole animation.

## Agent presentation

For all six, the large sidebar panel and phone banner are removed. The main navigation says **Agent version**, with the same muted styling as other navigation links. The footer repeats a quiet link. The agent landing page, Markdown alternates, structured profile, and writing files still work; only their promotion is reduced. Earlier studies remain available unchanged as comparison artifacts.

## Motion design

The main scene follows local scroll progress while the introduction is visible, so it completes before leaving the viewport. It uses a route reveal plus small changes in position, stride, wheel angle, headlamp, or scenery depending on the artwork. There are no click/drag controls.

The sticky masthead remains in normal document flow. Once the introduction leaves, it reveals a separate SVG illustration rather than a shrunken copy. That companion follows progress through the full homepage. There is no scroll interception, infinite animation, or autoplay. Passive scroll events are coalesced into one animation-frame update, and measured SVG route lengths are reused.

All six retain native links, keyboard/touch scrolling, selectable text, and visible focus. `prefers-reduced-motion` freezes the main art and hides the extra companion. Without JavaScript, the static main illustration and public-record links remain available. Article/history pages keep the quiet agent tab and static reading layouts; new motion is limited to the homepages in this review.

These are fictional landscape illustrations, not GPS tracks or claims about particular races, climbs, overnight expeditions, or pets. Personal copy remains a draft based on the user's supplied interests and experiences.

## Source and reproduction

- Original SVG sources: `art/<pair>-main.svg` and `art/<pair>-header.svg`.
- Shared appearance and motion: `assets/pairings.css`, `assets/pairings.js`.
- Shared page renderer: `templates/page.erb`, `../scripts/render-designs.rb`.
- Render all source changes with `./scripts/render-designs` from the repository root.
- Optional browser/capture check: `scripts/capture-pairings.py` with the documented Playwright environment and local server on port 4173.
- Screenshots: `assets/pair-*-main.png`, `assets/pair-*-header.png`, phone and full-page captures, plus `assets/pairings-comparison.png`.

The shared review checker covers local file links, named text colors, viewport overflow, and the agent handoff. Pair-specific checks cover distinct scenes, local and global progress, reversal, idle behavior, reduced motion, navigation overlap, unchanged core copy, and quieter agent links. See [QA.md](QA.md) for limits and commands.

The review folder remains excluded from Jekyll output. The public site's content and presentation have not been replaced.
