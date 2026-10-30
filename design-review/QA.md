# Prototype verification

Verified locally on October 28, 2026 using Playwright with Chromium 148 on macOS ARM. This does not verify the newer HTML-in-Canvas API, which these prototypes do not use.

## Passed

- Production `./scripts/check`: 32 generated HTML pages pass local link/asset validation; existing Sass deprecations remain.
- All 227 prototype HTML pages have valid local `href`/`src` file targets (220 direction pages, six comparison galleries, and the agent handoff page).
- All prototype pages fit at 320px, 768px, and 1440px without horizontal document overflow.
- Home, long-form reading, and history views checked in all three directions at desktop and 390px phone width.
- Full March 2026 article text is present in every direction. Original posts and production templates remain unchanged.
- Each history view contains the 13 existing timeline entries.
- Subject filters: Product returns 2 published entries, Systems returns 6, Everything restores all 8. The result count updates accessibly.
- With JavaScript disabled, all 8 entries remain visible and linked in the Field Guide.
- Skip-to-content link is the first keyboard focus target and navigates to main content.
- No JavaScript page errors during the primary home/article/history flows.
- Dark revision: self-hosted Plex Mono loads in served and direct-file previews.
- Main text, secondary text, and green accent tokens meet at least 4.5:1 against both background surfaces in every layout.
- Agent link appears in primary navigation and a prominent homepage panel; a mobile handoff link precedes the writing list.
- Agent prompt copies through the clipboard API; when clipboard access fails, the text is selected with keyboard-copy guidance.
- Structured record parses as JSON and contains 13 history entries and 8 writing records; 8 Markdown article exports exist.
- `design-review/` does not appear in Jekyll production output.
- Desktop home, phone home, and desktop reading screenshots captured for each direction; agent desktop/mobile and comparison gallery captured separately.

The broader viewport check found a legacy embedded-HTML sizing issue in the AUTCup article at 320px. Prototype CSS now allows grid children to shrink, constrains embedded media, and sizes old sharing SVGs without modifying the original article source.

## Personal variation checks

- Four additional variations generated from the selected blog, each with all eight articles and the full history.
- Cat and Ride introductions, writing lists, and sidebar text match the selected blog exactly; decorative illustration controls are separate.
- Cat wake/sleep toggle and pressed state pass; the awake cat responds to pointer movement.
- Bicycle route slider moves the rider with keyboard Home/End as well as dragging.
- Hiker advances through five trail positions, reaches the summit, and resets to the trailhead.
- Personal homepages checked at phone and desktop widths; all reading/history pages also pass the shared viewport checks.
- No-JavaScript version retains illustration, real writing links, and agent navigation.
- Reduced-motion preference disables the cat tail animation; route/hiker changes are immediate and user initiated.
- Desktop, phone, reading, and personal comparison screenshots are under `assets/`.
- Repeat with `python scripts/capture-personal.py` using the same Playwright environment and local server as below.

## Scroll study checks

- Three new homepage effects keep the selected Still Climbing introduction, writing, and sidebar copy unchanged. No illustration buttons or sliders remain in these variants.
- SVG positions change at the start, middle, and end of the page; scrolling back restores their initial position. They stop changing when scrolling stops.
- Keyboard PageDown updates the decorative progress through native scrolling.
- The summit miniature appears in the sticky masthead after the introduction exits and shares the hero hiker's progress. Its phone position does not overlap navigation.
- Phone screenshots and desktop start/middle/end captures are under `assets/scroll-*.png`.
- Reduced-motion preferences freeze the original mountain and hide extra margin/header motion in all three variants.
- No-JavaScript still exposes all eight posts, the original mountain, and agent navigation.
- Actual article reading pages remain static and retain their real content.
- Embedded live preview responds to its own scroll position in the comparison gallery.
- Repeat with `python scripts/capture-scroll.py` in the optional Playwright environment while the local server is running.

## Six main/header pairings

- Six new versions preserve the selected introduction, writing, and personal/professional sidebar text, while removing the large agent panel and mobile agent banner.
- Each has a working, unaccented “Agent version” main-navigation link and a quieter footer link. Article reading views retain the tab.
- All six main SVGs differ from their header SVGs. Main scenes change during early scrolling; header scenes change with full-page progress after the introduction exits.
- Scroll reversal restores the initial SVG state; stopping scroll stops updates. Native PageDown works.
- Header art does not overlap navigation at 320px, 390px, or 768px. All new pages also pass shared desktop/phone overflow checks.
- Original article body text remains present. New motion is scoped to the homepage studies.
- Reduced-motion settings freeze main scenes and hide extra header art in each variant. No-JavaScript preserves the illustration, all posts, and agent link.
- Screenshots capture each main scene, its distinct header, desktop and phone pages, and the comparison gallery. An expandable live preview is verified separately.
- Repeat with `python scripts/capture-pairings.py` in the optional Playwright environment while the local server is running.

## Three quieter ascents and portrait placement

- All three new homepages load the actual existing `img/kakto.jpg` and preserve the original image file. Intro, writing, and sidebar descriptions match High Pass apart from the added portrait/name caption.
- Portrait placements are an introduction identity block, personal sidebar, and a larger portrait where the main illustration previously sat.
- Main SVGs contain no bicycle, cyclist, or wheel graphics. There are no click/drag controls.
- Main cue travel is bounded to 16 SVG units; header travel to 12. The small stone rotates only 32 degrees. The cairn changes opacity without translating.
- Local and global scroll states change as intended, reverse back to the exact initial state, and stop when scrolling stops.
- Original photo and agent tab remain visible without JavaScript. Reduced-motion mode freezes the artwork and hides extra header motion.
- Header spacing passes at 320px, 390px, and 768px. Desktop/phone pages, tiny header details, and the comparison gallery are captured under `assets/quiet-*.png`.
- Real article bodies and quiet agent navigation are retained. Expandable live preview works.
- Repeat with `python scripts/capture-quiet.py` using the documented Playwright environment and local server.

## Three low mountain marks

- All three preserve the selected A Measured Ascent introduction, portrait placement, writing, sidebar, and quiet agent link.
- Main strips measure no more than 56px high at tested desktop, tablet, and phone widths.
- At 20% and 80% of the short local animation range, SVG states differ and the strip is verified to remain below the masthead and fully within the viewport. Tested at 1440×1000, 768×900, 390×844, and 320×568.
- The measured local scroll window is 48–96px. This explicitly resolves the old off-screen timing problem rather than only proving an SVG attribute changed.
- Reversal restores the initial artwork; stopping scroll stops header changes. The header cue appears as the strip passes the masthead and does not overlap navigation.
- Reduced-motion mode freezes the strip and hides the header cue; no-JavaScript retains the original photo and eight post links.
- Actual-size strips, early-scroll captures, full desktop/phone views, and the comparison gallery are under `assets/mountain-*.png` and `assets/mountains-comparison.png`.
- Expandable live preview is verified. Repeat with `python scripts/capture-mountains.py` in the optional Playwright environment while the local server runs.

## Limits

- These are lightweight prototypes, not a completed production migration.
- Safari/Firefox, screen-reader behavior, a full element-by-element contrast audit, and live external embeds were not comprehensively tested. Named text tokens were checked automatically.
- The full-page overflow audit blocks external requests for deterministic layout checks; external content may change independently.
- Existing pasted articles retain legacy markup. A production migration still needs individual embed/heading/attribution review.
- Current CTO title dates and preferred final biography have not been confirmed.
- Prototype Markdown exports retain meaningful original embedded HTML; this is not a conversion of every historical embed into an agent-readable description.
- No production agent endpoint, deployment pipeline change, or new public website has been published.

## Repeat the checks

The website itself has no Node or Playwright dependency. These optional QA helpers use Python Playwright, installed outside the repository:

```sh
python3 -m venv /tmp/mario-design-qa-venv
/tmp/mario-design-qa-venv/bin/pip install playwright
/tmp/mario-design-qa-venv/bin/python -m playwright install chromium
./scripts/render-designs
python3 -m http.server 4173 --bind 127.0.0.1
```

With that server running, in another terminal from the repo root:

```sh
/tmp/mario-design-qa-venv/bin/python scripts/check-designs.py
/tmp/mario-design-qa-venv/bin/python scripts/capture-designs.py
```

`capture-designs.py` accepts an optional base URL ending at the review directory. `check-designs.py` uses the documented local URL. Screenshots are written under `design-review/assets/`; capture the gallery after direction screenshots so its thumbnails are current. Stop the local server after reviewing.

## Implementation checkpoint — October 29, 2026

- Selected Thin Ridgeline recorded in `selected.json`; all referenced source, screenshots, font licenses, and handoff files exist.
- Re-rendered all 22 design variants from source; shared browser checks pass across 227 review HTML pages.
- Re-ran the selected mountain/portrait/on-screen scroll checks successfully.
- Production build and link checks pass; review artifacts and AGENTS.md are excluded from `_site/`. Existing Sass deprecations remain.
- Captured 61 required public outputs, including all eight existing post routes, in `production-routes.json`. `./scripts/check` now runs the preservation guard.
- Verified the guard rejects a missing original post using an isolated copy of the actual build; the real post and production output were not removed.
- Read-only GitHub Pages inspection confirms legacy publishing from `master` at `/`, custom domain `mariomendez.me`, HTTPS enforced. No hosting settings changed.
- Production template port, public agent exports, media-kind switching, and hosting build parity are documented next steps, not completed features of this checkpoint.


## Production release audit — October 29, 2026

The selected design is now ported to the live Jekyll templates on `redesign/thin-ridgeline`. This section supersedes prototype-only limitations above where explicitly covered.

- `./scripts/check` passes: 34 HTML pages, local links/assets/responsive image candidates, all 61 baseline outputs and eight post URLs, JSON/XML, profile/history/article parity, structured data, social-link new-tab notices, and development-file exclusions.
- Chromium checks cover every generated HTML page at 320, 390, 768, and 1440px: no document overflow, no missing images, one main heading, valid structured data, safe GitHub/LinkedIn targets and indicators, and keyboard access to the skip link. Homepage photo placement/width matches the approved desktop and mobile behavior. Screenshots for home, experience, archive, agents, and an article are under `/tmp/mario-production-*.png`.
- Isolated builds exercise ridgeline, image, and no-media modes at all four widths. The portrait and all eight writing links remain; only ridgeline mode loads its controller. Reduced-motion and no-JavaScript reading checks pass.
- All nine broken university-hosted article photos were recovered as actual JPEGs from archived copies and self-hosted. Their source/archival URLs are retained in `recovered-media.json`; article source snapshots are in `archived-article-sources.json`. Copied article text and attribution were compared before/after and preserved. Nonfunctional copied sharing widgets/scripts were removed; video URLs remain intact with accessible iframe titles.
- The lab experience image uses an official University of Manitoba logo suitable for a dark background, replacing the illegible lab banner. Source recorded in `asset-sources.json`.
- Current timeline spelling/grammar was corrected without changing dates or factual claims. Experience identifiers now remain stable when a title is edited. Profile JSON exports plain text rather than HTML for personal interests.
- External checks returned HTTP 200 for the final article/profile links, archived source articles, GitHub links, conference history, and YouTube embed endpoints. LinkedIn returns HTTP 999 to automated requests, so its destination could not be automatically verified. Successful YouTube responses do not establish playback availability in every region/account.
- Native Pages remains a legacy build from `master` at `/`, custom domain `mariomendez.me`, HTTPS enforced. No publishing setting was changed. The deployment workflow uses the locked Ruby/Bundler/Jekyll build, runs generation and validation, uploads that exact output, and deploys only from `master`; its build job explicitly has Pages read permission.

Release sequence: switch Pages source to **GitHub Actions** at the approved release, immediately before merging this branch into `master`; verify the deployment workflow succeeds and check the live homepage, experience, one old and one new article, agent downloads, custom-domain HTTPS, and 404. Retain the previous commit as the rollback point. Local/branch CI success does not demonstrate a completed live deployment.

Limits: the visual/browser audit uses Chromium, not a full Safari/Firefox or assistive-technology matrix. External services and archived sources can change independently. The existing 2024 CTO period and April 2022–2023 lead-developer period are retained as supplied; no intervening dates were inferred.


### Agent prompt URL regression

The generic static server previously used for port 4175 served a production build. Its clickable download links resolved locally, but absolute URLs inside the prompt and downloads pointed at the public domain, where the new files do not exist until release. The active preview now uses `./scripts/serve --port 4175 --destination /tmp/mario-site-preview`; development-mode URLs use the actual preview port throughout. Production builds retain canonical HTTPS endpoints.

`scripts/check-agent-links.py` follows all internal agent-screen links, three prompt URLs, four exports, and all eight article/Markdown pairs over HTTP (28 unique local URLs). It verifies plain-text downloads, JSON, export titles, and prompt copy behavior. `./scripts/check` now also verifies the URLs embedded in the prompt against the build configuration and confirms each referenced file exists. The HTTP check must use a development preview before deployment, or the real public domain after deployment.
