# Implement the selected website

Updated October 29, 2026 · branch `redesign/thin-ridgeline`

**Implementation update:** The production port described below is now implemented on this branch. See the root README for the current structure and commands. The original handoff below records the approved design and acceptance criteria. Hosting/build parity and release remain outstanding.

## Start here

The design exploration is finished for now. **Thin Ridgeline**, built on **A Measured Ascent**, is the approved visual reference. It is a reference name, not the public site's brand. Do not restart with another direction or merge features from older galleries by default.

- [Selected homepage](mountain-ridge/index.html)
- [Selected article treatment](mountain-ridge/road-to-seed-round.html)
- [Selected history treatment](mountain-ridge/history.html)
- [Desktop capture](assets/mountain-ridge-desktop.png) and [phone capture](assets/mountain-ridge-mobile.png)
- [Machine-readable selection](selected.json)
- [Existing URL contract](production-routes.json)

This branch contains the complete local exploration, editable source, licensed fonts, generated review pages, screenshots, and browser checks. The public Jekyll layouts are still the old theme. **The task ahead is a production port, not publishing the standalone prototype.**

## Settled decisions

Use a black background, off-white text, restrained green links, and locally hosted IBM Plex Mono. Keep the compact introduction, writing-first homepage, complete archive, professional history, and quiet navigation. Preserve the original `img/kakto.jpg` portrait beside the introductory heading. Keep the actual posts and their URLs.

“Agent version” belongs in the top-level navigation with the same subdued treatment as the other links. Do not restore the large sidebar panel, mobile banner, or promotional agent copy from earlier studies. The destination still needs to be useful: readable profile, history, Markdown writing, JSON, and a copyable prompt using public URLs.

The thin mountain strip is **temporary optional media**. Mario expects to replace it with another personal photograph eventually. Do not require that photograph to begin or finish the initial port. Preserve the existing headshot independently of this slot. The slot must support a ridgeline, an ordinary responsive image, or no media; its presence must not determine whether the writing/layout works.

The optional ridgeline is a shallow 52–56px mark, with no moving figure, dot, bicycle, stone, or route. Its small movement occurs in a measured 48–96px scroll window while visible; a small companion appears in the floating masthead as it leaves. Respect reduced motion and retain static/no-JavaScript reading. The selected behavior is `assets/mountains.js`, not the older climb/ride controllers.

## Where the source is

| Reference source | Production use |
| --- | --- |
| `templates/page.erb` | Translate the selected DOM structure into shared Jekyll/Liquid templates |
| `assets/styles.css` | Base tokens, typography, reading layout, archive and history foundations |
| `assets/personal.css`, `pairings.css`, `quiet.css`, `mountains.css` | Selected overrides only; consolidate instead of shipping the entire exploration cascade |
| `assets/mountains.js` | Optional ridgeline behavior; adapt selectors to one production media component |
| `art/mountain-ridge-main.svg`, `art/mountain-ridge-header.svg` | Current replaceable feature graphic and companion |
| `assets/fonts/IBMPlexMono-{Regular,Medium}.ttf`, `IBM-Plex-Mono-OFL.txt` | Self-host selected fonts and retain the license |
| `_posts/`, `_config.yml` events/social data, existing images | Actual content and assets; keep source authoring in Jekyll |
| `profile.md`, `profile.json`, `writing.md`, `llms.txt`, `text/` | Prototype agent representations demonstrating the contract; rebuild from production sources |

The prototype renderer deliberately carries many alternative branches, hard-coded editorial summaries, and review-only markup. Do not make it the production rendering pipeline. Do not copy generated article HTML back into `_posts/`, ship all prior animations/fonts, or retain relative paths that only work inside `design-review/`.

## Implementation sequence

### 1. Port the visual foundation

Create one shared Jekyll document layout and small includes for navigation, identity, optional feature media, and footer. Add a consolidated site stylesheet and the two selected font files/license. Use `relative_url`/`absolute_url` for generated paths, rather than prototype `../` or hard-coded local preview links. Keep layout and content available before JavaScript.

Introduce a small public profile data file, for example `_data/profile.yml`, with the portrait and optional feature media as separate fields:

```yaml
portrait:
  src: /img/kakto.jpg
  alt: Mario Mendez
feature_media:
  kind: ridgeline # ridgeline | image | none
  src: null
  alt: null
```

Only render/load the ridgeline controller for `kind: ridgeline`. An image should use explicit dimensions, useful alt text, and a bounded responsive presentation. No fullscreen photo background, new image requirement, or animation dependency should be introduced. Future image framing can be decided when Mario supplies the asset.

### 2. Migrate the actual pages

Rework the real homepage, `/blog/` archive, post layout, and category/tag templates using the selected treatment. Add `/experience/` using structured entries, retaining overlapping work/research periods. Preserve legacy section URLs such as `/about.html` and `/timeline.html` with useful content or deliberate compatibility redirects if replacing them with new routes.

Replace old theme dependencies only after live templates stop using them. Core reading/navigation should need no Bootstrap, jQuery, external font service, or animation library. Preserve necessary license attribution. Retain feed, sitemap, 404, favicon, web manifest, and custom domain support.

Review long titles and old pasted HTML: some posts carry their own headings, HTTP media, inline dimensions, and copied share scripts. Adapt presentation without silently losing article text, attribution, images, or video. Do not carry unused share/comment/analytics integrations into the new shared shell by accident.

### 3. Publish human and agent views from the same sources

Render `/for-agents/`, `/profile.md`, `/profile.json`, `/writing.md`, `/llms.txt`, and per-article Markdown alternates from the same profile/history/posts as the HTML. The prompt should point to real HTTPS endpoints after release; the attachment-based prompt in the prototype is explicitly local review copy.

Give JSON a schema version, canonical URLs, publish/update dates, and stable identifiers. Add appropriate Person/ProfilePage and BlogPosting structured data. Keep feed/sitemap discovery. Do not invent exact CTO start dates or infer promotion/founding dates from the old timeline. Current user-supplied facts include CTO/founder, software/product/team interests, cats, several marathons, and multi-day rides. The prototype profile export is a reference, not an independent biography to maintain.

A public read-only site does not need an MCP server or a chatbot to support agents. Static readable files and semantic HTML are the initial implementation.

### 4. Verify the migration before release

`./scripts/check` now builds, checks internal HTML links/assets, and verifies **61 protected public outputs**, including all **8 existing post routes**, discovery/hosting files, and old image paths. The guard reads `production-routes.json`. Do not erase entries to make a failing migration pass; retain each output or provide an intentional compatibility redirect at that path. This checks file presence, not redirect destinations or content fidelity.

Use the selected visual references and `scripts/capture-mountains.py` for motion/layout behavior. Adapt those checks to the real routes when porting; the current script targets the review directory. Keep the original source of a useful check even when replacing its prototype URL. The optional Playwright setup and verification limits are in [QA.md](QA.md).

Validate at least:

- Homepage, archive, a long post, the oldest HTML-heavy post, history, tag/category archives, and 404 at phone/tablet/desktop widths.
- Original headshot placement, muted links, wrapping, keyboard focus, contrast, and no horizontal overflow.
- Native scrolling, visible early ridgeline motion, header/nav separation, reduced motion, and no-JavaScript reading.
- `feature_media.kind` set to `ridgeline`, `image`, and `none`; switching must not remove the portrait, break navigation, or throw script errors.
- Agent HTML/Markdown/JSON parity, valid JSON/XML, canonical URLs, real Markdown alternates, and a prompt that can retrieve the public sources.
- Old routes still resolve, posts/media remain intact, and no review galleries, source tooling, or private metadata appears in production output.

### 5. Confirm the publishing path and release

Hosting was checked read-only on **2026-10-29** with:

```sh
gh api repos/mariowr2/mariowr2.github.io/pages
```

GitHub returned `build_type: legacy`, source `master` at `/`, custom domain `mariomendez.me`, HTTPS enforced, status `built`. The checked-in Actions workflow only validates. A push to this redesign branch does not select it as the Pages source; merging into `master` can update the live site through the legacy Pages build.

Resolve build parity before merging. Local dependencies pin Jekyll 4.4.1, while native Pages chooses its own supported environment. Either verify the final code against that environment or implement an explicit Actions-based Pages build/deploy using the locked dependencies, and change the Pages source as part of the actual release. Do not assume adding a validation job publishes anything or silently change hosting during a styling port.

## First concrete implementation slice

The best next coding task is the shared Jekyll layout + stylesheet/fonts + homepage port, with separate portrait/feature-media fields. Review that page against `mountain-ridge/index.html` before expanding to post/archive/history templates. This produces a real maintainable page without replacing the content pipeline or repeating the design exploration.

## What is done / what remains

Done: selected reference recorded, all prototypes/source/assets captured, branch isolated, hosting verified, route contract captured, URL guard added to the normal CI command, browser checks preserved, and migration order/acceptance criteria documented.

Remaining: port real Jekyll templates, introduce shared public profile data, integrate production agent exports, consolidate assets/remove unused theme dependencies, verify hosting build parity, and release the chosen site. No new public website or production agent endpoints have been deployed by this checkpoint.
