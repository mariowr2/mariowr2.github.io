# Working in this repository

Read README.md for setup, architecture, commands, and known limitations.

- This is a Jekyll static site, not a Node application. Use Ruby from `.ruby-version`, dependencies from `Gemfile.lock`, and the `scripts/` entry points.
- Edit source templates/content/assets, not `_site/` or caches. Keep development tooling out of published output via `_config.yml` exclusions.
- Before committing, run `./scripts/check`. Include generated `categories/` and `tags/` source pages in the commit. CI verifies these are current.
- Archive generation runs before build/serve, not continuously inside Jekyll's watcher. Restart preview after adding new taxonomy values or changing configuration.
- Preserve existing post URLs, content, and embedded media during redesigns unless the task calls for changes. Dates, filenames, and categories affect routes.
- Homepage order and timeline data live in `_config.yml`; shared markup and inline JavaScript live in `_includes/`; styles live in `css/` and `_sass/`.
- The production build currently emits Sass deprecation warnings. Frontend dependency modernization is deferred; avoid unrelated theme rewrites during maintenance.
- CI only validates; deployment settings have not been verified. Do not assume a push or a successful check publishes the site.
- Do not run the inherited `scripts/integrate-personal` upstream merge helper as routine setup.
