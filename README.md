# Mario Mendez's website

Static personal website and blog for https://mariomendez.me, built with Jekyll and the MIT-licensed Personal theme (derived from Grayscale/Timeline). No backend, database, or Node toolchain is required.

## Setup

Install Ruby **4.0.9** using your preferred Ruby version manager (`.ruby-version`), then install Bundler **4.0.23** if it is missing:

```sh
gem install bundler -v 4.0.23
./scripts/install
./scripts/serve
```

Open http://127.0.0.1:4000. Dependencies are declared in `Gemfile` and pinned in `Gemfile.lock`, including Mac ARM and Linux x86_64 platforms. Do not use `sudo gem install` or install Jekyll globally for this project.

## Commands

Run these from the repository root:

| Command | Purpose |
| --- | --- |
| `./scripts/install` | Install the locked Ruby dependencies |
| `./scripts/serve` | Watch and preview locally, without production analytics |
| `./scripts/serve-production` | Preview production template behavior locally |
| `./scripts/serve-lan` | Preview on the local network at your machine's IP, port 4000 |
| `./scripts/serve-lan-production` | LAN preview with production template behavior |
| `./scripts/build` | Generate archive sources and build production output into `_site/` |
| `./scripts/check` | Production build, local links/assets, and preserved public URLs |
| `bundle exec ruby scripts/generate-archives` | Refresh category and tag source pages |
| `./scripts/newpost my-post-slug` | Create a post skeleton; edit its front matter and body |

Serve/build scripts accept additional Jekyll arguments, for example `./scripts/serve --port 4001`. Restart the server after configuration changes. Adding a new tag or category also requires restarting the preview or running the archive generator before Jekyll rebuilds.

Local previews layer `_config.dev.yml` over `_config.yml`, disable HTTPS redirection, and use a local canonical URL. For another port or LAN hostname, supply `--url http://YOUR_HOST:PORT`. Production builds use only `_config.yml` and its public domain. LAN preview binds to all interfaces; firewall changes, if needed, are managed outside these scripts.

## Structure

- `_config.yml`: metadata, social links, homepage writing order and roles, professional timeline, and build settings.
- `_data/profile.yml`: shared public biography, original portrait, and independent optional feature media (`ridgeline`, `image`, or `none`). Image mode uses `src`, `alt`, `width`, and `height`; no new photo is required.
- `_data/writing.yml`: selected writing summaries shared by homepage and articles.
- `_layouts/default.html`, `_includes/site-nav.html`: shared semantic document, navigation, discovery, structured data, and footer.
- `assets/site.css`, `assets/fonts/`, `assets/ridgeline.js`: consolidated design, licensed local IBM Plex Mono, and optional homepage movement. The site shell has no external frontend dependencies.
- `_posts/`: original dated Markdown and embedded HTML/media, with unchanged public URLs.
- `categories/`, `tags/`, `text/`: committed generated taxonomy pages and raw Markdown article alternates. Build/serve scripts regenerate these from posts; CI checks they are current.
- `/experience/`: full timeline from `_config.yml`, retaining overlapping periods.
- `/for-agents/`, `/profile.md`, `/profile.json`, `/writing.md`, `/llms.txt`: public representations of the same profile, history, and posts. Markdown source templates use `.html` filenames with explicit `.md` permalinks to avoid Jekyll converting them to HTML.
- `design-review/`: archived references, handoff, screenshots, and route preservation contract; excluded from publication.
- `css/`, `_sass/`, `js/`, older includes: retained theme sources; old `css/` and `js/` assets are excluded from publication.
- `_site/`, `.jekyll-cache/`, `.bundle/`: generated/local files, ignored by Git.

Post filenames determine dates/slugs; categories also affect default Jekyll post URLs. Preserve existing URLs or add redirects when migrating content. Archive links retain lowercase names and encode spaces.

## Validation and CI

Run `./scripts/check` before committing, and commit any generated category/tag pages. GitHub Actions runs the same check and rejects uncommitted archive generation changes. The checker validates local `href`/`src` targets and `srcset` image candidates, including absolute links to the configured public domain. It skips external URLs and fragment IDs; it does not inspect CSS URLs, JavaScript behavior, or remote embeds. Preview affected pages on desktop and mobile for visual changes.

The redesigned shell uses local fonts, CSS, and optional vanilla JavaScript. Inherited analytics, comments, sharing widgets, Bootstrap, jQuery, and external font services are absent from the shared layouts. Historical posts retain their text, attribution, and video URLs. Broken university-hosted photos have been recovered from the Internet Archive and are served locally; their original URLs and archived copies are recorded in `design-review/recovered-media.json`. Copied third-party sharing controls/scripts were removed. The retired article source links now point to archived originals, and conference links point to current official history pages. Remote video availability remains outside deterministic local checks.

Optional browser verification: serve `_site/` at `http://127.0.0.1:4175`, then run `scripts/check-redesign.py` with Python Playwright installed outside the site runtime (see `design-review/QA.md`). It checks all posts and principal pages at 320, 390, 768, and 1440px, visible ridgeline movement, reversal, masthead separation, reduced motion, no-JavaScript reading, structured data, and prompt copy. Desktop/phone screenshots go to `/tmp/mario-production-{width}.png`. `scripts/check-redesign-media.py` builds ridgeline/image/none configurations in temporary directories and verifies they retain the portrait and writing; it also checks source/history parity. `./scripts/check` validates Markdown/JSON parity, structured data, XML, responsive image targets, social-link behavior, and exclusion of development artifacts. Both require permission to launch Chromium outside a restricted sandbox.

## Hosting

GitHub Pages uses the custom domain `mariomendez.me`. The new `.github/workflows/deploy.yml` builds and deploys only from `master` (including manual runs). Each deployment runs `./scripts/check`, which regenerates category/tag pages and article Markdown from current posts, builds with `.ruby-version` and `Gemfile.lock`, and validates links and protected routes. Only that validated `_site/` artifact is uploaded and deployed. Profile Markdown/JSON, writing indexes, and `llms.txt` render from shared sources during the same build. Deployment does not rely on generated files already being current in Git.

**Release activation:** Pages was rechecked on October 29, 2026 and still uses the legacy build from `master` at `/`, with HTTPS enforced. At the approved release, switch repository Settings → Pages → Build and deployment → Source to **GitHub Actions** immediately before merging this branch into `master`. The merge then triggers the locked build and deployment. If the workflow is already on `master`, switch the source and run “Deploy GitHub Pages” on `master`. Switching before the merge avoids an unintended legacy build publishing the redesign first. This replaces the legacy Jekyll environment with the locked build. Until that setting changes, the new publishing path is not active. No hosting settings were changed during implementation. Merging into `master` while legacy publishing remains enabled can still publish through the old build path.

Pull requests and branch pushes continue to run `.github/workflows/check.yml` for validation; they cannot deploy through the new workflow.

`scripts/integrate-personal` is an inherited upstream merge helper, not part of the normal development workflow. Do not run it during routine maintenance.

## Selected redesign and implementation handoff

The selected direction is **Thin Ridgeline**, built on A Measured Ascent: dark background, off-white text, restrained green links, self-hosted IBM Plex Mono, and the original portrait beside the introduction. The original mountain is now replaced by Mario’s full-resolution alpine cycling photograph, with responsive JPEG variants and a full-size link. It aligns with the personal sidebar on desktop and appears immediately before the personal text on mobile. The component still supports a ridgeline or no media independently of the portrait. “Agent version” is a quiet top-level navigation link.

Start implementation with [the handoff](design-review/HANDOFF.md) and [the recorded selection](design-review/selected.json). The approved [homepage](design-review/mountain-ridge/index.html), [reading view](design-review/mountain-ridge/road-to-seed-round.html), [history view](design-review/mountain-ridge/history.html), and desktop/phone captures are committed references. Older galleries are design history, not competing specifications.

The production templates now implement the selected reference. The original handoff remains the design record and release checklist. The homepage, article, archive, taxonomy, experience, compatibility pages, and agent endpoints are implemented; an explicit locked-dependency deployment workflow is included; hosting activation and actual release remain outstanding steps. No hosting settings were changed during the port.

Run `./scripts/check` before committing. It now also checks [the existing public URL contract](design-review/production-routes.json): 61 required outputs, including all eight current post routes, discovery/hosting files, and original images. Missing paths fail local checks and the existing CI workflow. Preserve a route or add its intentional compatibility redirect when changing the structure.

To preview the selected artifact, open `design-review/mountain-ridge/index.html` directly, or serve the repository:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Then visit http://127.0.0.1:4173/design-review/mountain-ridge/ . Run `./scripts/render-designs` to regenerate review HTML and agent examples from the current posts and timeline. Shared ERB source is in `design-review/templates/`, with licensed fonts, SVGs, styles, and scripts under `design-review/`. The directory is excluded from production output.

Optional browser checks and captures use Python Playwright outside the site runtime. See [QA.md](design-review/QA.md) for setup, the production audit, and limits; `scripts/check-designs.py` checks the whole review and `scripts/capture-mountains.py` covers the selected portrait/layout, low graphic, on-screen timing, and reduced motion. Preserve/adapt these checks to the real URLs during the port.
