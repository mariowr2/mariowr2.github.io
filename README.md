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
| `./scripts/check` | Production build followed by local HTML link/asset checks |
| `bundle exec ruby scripts/generate-archives` | Refresh category and tag source pages |
| `./scripts/newpost my-post-slug` | Create a post skeleton; edit its front matter and body |

Serve/build scripts accept additional Jekyll arguments, for example `./scripts/serve --port 4001`. Restart the server after configuration changes. Adding a new tag or category also requires restarting the preview or running the archive generator before Jekyll rebuilds.

Local previews layer `_config.dev.yml` over `_config.yml`, disable HTTPS redirection, and use a local canonical URL. For another port or LAN hostname, supply `--url http://YOUR_HOST:PORT`. Production builds use only `_config.yml` and its public domain. LAN preview binds to all interfaces; firewall changes, if needed, are managed outside these scripts.

## Structure

- `_config.yml`: public URL, metadata, homepage section order (`pages_list`), social links, timeline events, and plugin settings.
- `index.html` and `_layouts/index.html`: homepage entry point and composition. Root section files such as `about.html` supply content/front matter to matching `_includes/` sections.
- `_layouts/`: blog, post, archive, and error templates.
- `_includes/`: shared navigation, head, footer, section markup, and JavaScript.
- `_posts/`: dated Markdown posts, some with substantial embedded HTML and third-party media.
- `categories/` and `tags/`: committed archive source pages. Build/serve scripts generate missing/current entries from post metadata. Existing unused pages are retained to preserve URLs; remove intentionally if desired.
- `css/` and `_sass/`: Sass styles, variables, and mixins; `img/` and `js/`: static assets.
- `_site/`, `.jekyll-cache/`, and `.bundle/`: generated/local files, ignored by Git.

Post filenames determine dates/slugs; categories also affect default Jekyll post URLs. Preserve existing URLs or add redirects when migrating content. Archive links retain lowercase names and encode spaces.

## Validation and CI

Run `./scripts/check` before committing, and commit any generated category/tag pages. GitHub Actions runs the same check and rejects uncommitted archive generation changes. The checker validates local `href`/`src` file targets, including absolute links to the configured public domain. It skips external URLs and fragment IDs; it does not inspect CSS URLs, `srcset`, JavaScript behavior, or remote embeds. Preview affected pages on desktop and mobile for visual changes.

The baseline build succeeds but reports Sass deprecations (`@import` and `darken`). Bootstrap 3, jQuery 1, Font Awesome 4, and several scripts/fonts still load from external CDNs. Modernizing these is deferred to the redesign. Some posts contain copied third-party HTML, HTTP images, or legacy sharing markup. The production analytics configuration is also inherited and should be revisited during the redesign.

## Hosting

The repository name and `CNAME` indicate GitHub Pages with custom domain `mariomendez.me`. Actual Pages source/branch settings live in GitHub and have not been verified. The checked-in workflow validates changes; it **does not deploy**. Confirm hosting settings before changing the publishing pipeline. Native GitHub Pages may use different dependency versions from the locally locked Jekyll 4 setup; use a custom build/deploy workflow if exact parity is required.

`scripts/integrate-personal` is an inherited upstream merge helper, not part of the normal development workflow. Do not run it during routine maintenance.
