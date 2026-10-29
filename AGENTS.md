# Working in this repository

Read README.md for setup, architecture, commands, and known limitations.

For the redesign, read `design-review/HANDOFF.md` and `design-review/selected.json` first. Thin Ridgeline / A Measured Ascent is the selected reference; earlier alternatives are archived exploration. Preserve the original portrait. Treat the mountain as optional replaceable feature media, separate from the portrait, so a future personal photo does not require a new layout or controller. Keep agent promotion to a quiet “Agent version” navigation link. The production template port remains to be done.

- This is a Jekyll static site, not a Node application. Use Ruby from `.ruby-version`, dependencies from `Gemfile.lock`, and the `scripts/` entry points.
- Edit source templates/content/assets, not `_site/` or caches. Keep development tooling out of published output via `_config.yml` exclusions.
- Before committing, run `./scripts/check`. Include generated `categories/` and `tags/` source pages in the commit. CI verifies these are current. The check also protects the existing public outputs in `design-review/production-routes.json`; preserve paths or add deliberate compatibility redirects rather than deleting baseline entries to silence failures.
- Archive generation runs before build/serve, not continuously inside Jekyll's watcher. Restart preview after adding new taxonomy values or changing configuration.
- Preserve existing post URLs, content, and embedded media during redesigns unless the task calls for changes. Dates, filenames, and categories affect routes.
- Homepage order and timeline data live in `_config.yml`; shared markup and inline JavaScript live in `_includes/`; styles live in `css/` and `_sass/`.
- The production build currently emits Sass deprecation warnings. Frontend modernization belongs to the selected redesign port; avoid unrelated theme rewrites during maintenance.
- CI only validates. Pages was verified on 2026-10-29 as a legacy build from `master` at `/`; merging there can publish through native Pages. Resolve locked-Jekyll/build parity and recheck hosting settings before release. A successful validation job is not a deployment.
- Do not run the inherited `scripts/integrate-personal` upstream merge helper as routine setup.
