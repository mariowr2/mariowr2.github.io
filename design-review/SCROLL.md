# Scroll studies on Still Climbing

The user selected Still Climbing and asked to replace click-to-move interactions with three scroll-driven alternatives. The introduction, writing, sidebar, and professional history remain the same across the new versions. There are no illustration buttons or sliders.

## Three options

- **[A bike in the margin](scroll-bike/index.html):** a small side-on bicycle travels vertically down a faint rail in the left margin. Wheel rotation follows page progress; scrolling up reverses it. The original mountain remains a static illustration.
- **[The summit companion](scroll-summit/index.html):** a hiker follows the existing mountain trail according to full-page scroll progress. Once the introduction has left view, the same mountain appears in miniature in the sticky masthead. Both share the same progress, and the summit corresponds to the end of the homepage.
- **[A trail through the writing](scroll-trail/index.html):** an understated winding trail runs in the outside margin, with dots aligned to real posts. The visited line draws as the reader scrolls; a small runner follows the approximate reading position. The original mountain remains static.

Review all three live at [motion.html](motion.html). The embedded frames are actual pages, not recordings: scroll inside one or use the full-page links. Original personal options remain at [personal.html](personal.html).

## Behavior and constraints

- Motion is decorative. Normal links, keyboard scrolling, touch scrolling, find-in-page, selection, and agent access remain native.
- All changes follow user scrolling. No autoplay, perpetual animation, scroll interception, snap scrolling, or easing loop is used.
- Scroll listeners are passive and coalesced into one `requestAnimationFrame` update. Geometry is measured on load, fonts-ready, and resize; each scroll update changes SVG attributes instead of rebuilding the page.
- Bike/trail gutters reserve space on smaller screens. The sticky summit miniature sits in the masthead; it does not cover post text or navigation. Shorter screens get less travel distance, not artificially extended pages.
- `prefers-reduced-motion` hides the extra margin/header motion and retains the static hero mountain. JavaScript off retains the original page, illustration, and links.
- New effects are limited to homepage studies. All eight full article reading views and history pages remain available with static layouts.
- Illustrations imply no GPS route, elevation, race result, or mountain-climbing claim.
- This is local review work, excluded from Jekyll production output.

## Sources and regeneration

New variants extend the selected summit data in `scripts/render-designs.rb`. Their generated pages live in `scroll-bike/`, `scroll-summit/`, and `scroll-trail/`. Motion code is in `assets/scroll.js` and `assets/scroll.css`; the mountain illustration remains in `templates/personal-scene.erb`. Render with `./scripts/render-designs`.

For browser checks, start the documented local server at port 4173 and run `scripts/capture-scroll.py` using the optional Playwright Python environment described in [QA.md](QA.md). Screenshots at the start, middle, and end plus phone captures are under `assets/`. Shared `scripts/check-designs.py` covers all review HTML links, text contrast tokens, viewport overflow, and agent handoff behavior.

## Recommendation

The summit companion is the clearest continuation of the selected design. The bike is a more playful personal detail. The trail adds the most visible structure and should remain subtle to avoid returning to the original site's oversized timeline treatment.
