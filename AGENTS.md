# Working in this repository

Read README.md for setup, architecture, commands, and known limitations.

The production redesign is implemented. Preserve its dark palette, self-hosted IBM Plex Mono, original portrait, and quiet “Agent version” navigation. The optional feature photograph is independent of the portrait; support image or no media. Prototype artifacts and controllers are intentionally omitted. Read `docs/QA.md` for verification and release notes.

- This is a Jekyll static site, not a Node application. Use Ruby from `.ruby-version`, dependencies from `Gemfile.lock`, and the `scripts/` entry points.
- Edit source templates/content/assets, not `_site/` or caches. Keep development tooling out of published output via `_config.yml` exclusions.
- Before committing, run `./scripts/check`. Include generated `categories/` and `tags/` source pages in the commit. CI verifies these are current. The check also protects the existing public outputs in `docs/production-routes.json`; preserve paths or add deliberate compatibility redirects rather than deleting baseline entries to silence failures.
- Archive generation runs before build/serve, not continuously inside Jekyll's watcher. Restart preview after adding new taxonomy values or changing configuration.
- Preserve existing post URLs, content, and embedded media during redesigns unless the task calls for changes. Dates, filenames, and categories affect routes.
- Homepage order and timeline data live in `_config.yml`; shared markup lives in `_includes/`; styles and JavaScript live in `assets/`.
- The validation workflow only validates. The deployment workflow builds with locked dependencies and publishes from `master` once Pages is switched to GitHub Actions. Pages was last verified on 2026-10-29 as legacy publishing from `master` at `/`; recheck settings at release. A successful validation job is not a deployment.
- Do not run the inherited `scripts/integrate-personal` upstream merge helper as routine setup.
