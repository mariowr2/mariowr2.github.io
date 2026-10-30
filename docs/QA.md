# Production verification

Build with `./scripts/check`. Preview with `./scripts/serve --port 4175 --destination /tmp/mario-site-preview`.

Optional browser checks use Python Playwright outside the site runtime:

```sh
python3 -m venv /tmp/mario-site-qa
/tmp/mario-site-qa/bin/pip install playwright
/tmp/mario-site-qa/bin/python -m playwright install chromium
/tmp/mario-site-qa/bin/python scripts/check-redesign.py
/tmp/mario-site-qa/bin/python scripts/check-redesign-media.py
/tmp/mario-site-qa/bin/python scripts/check-agent-links.py
```

Browser captures are written to `/tmp/` and are not committed. The browser checks expect a running preview on port 4175. The media-mode check creates its own isolated temporary builds.

## Production release audit — October 29, 2026

The production templates implement the approved design on `redesign/thin-ridgeline`. Prototype galleries, screenshots, artwork, and generators are omitted from the production branch.

- `./scripts/check` passes: 34 HTML pages, local links/assets/responsive image candidates, all 61 baseline outputs and eight post URLs, JSON/XML, profile/history/article parity, structured data, social-link new-tab notices, and development-file exclusions.
- Chromium checks cover every generated HTML page at 320, 390, 768, and 1440px: no document overflow, no missing images, one main heading, valid structured data, safe GitHub/LinkedIn targets and indicators, and keyboard access to the skip link. Homepage photo placement/width matches the approved desktop and mobile behavior. Screenshots for home, experience, archive, agents, and an article are under `/tmp/mario-production-*.png`.
- Isolated builds exercise image and no-media modes at all four widths. The portrait and all eight writing links remain. No-JavaScript reading checks pass.
- All nine broken university-hosted article photos were recovered as actual JPEGs from archived copies and self-hosted. Their source/archival URLs are retained in `recovered-media.json`; article source snapshots are in `archived-article-sources.json`. Copied article text and attribution were compared before/after and preserved. Nonfunctional copied sharing widgets/scripts were removed; video URLs remain intact with accessible iframe titles.
- The lab experience image uses an official University of Manitoba logo suitable for a dark background. Source recorded in `asset-sources.json`.
- Current timeline spelling/grammar was corrected without changing dates or factual claims. Experience identifiers now remain stable when a title is edited. Profile JSON exports plain text rather than HTML for personal interests.
- External checks returned HTTP 200 for the final article/profile links, archived source articles, GitHub links, conference history, and YouTube embed endpoints. LinkedIn returns HTTP 999 to automated requests, so its destination could not be automatically verified. Successful YouTube responses do not establish playback availability in every region/account.
- Native Pages remains a legacy build from `master` at `/`, custom domain `mariomendez.me`, HTTPS enforced. No publishing setting was changed. The deployment workflow uses the locked Ruby/Bundler/Jekyll build, runs generation and validation, uploads that exact output, and deploys only from `master`; its build job explicitly has Pages read permission.

Release sequence: switch Pages source to **GitHub Actions** at the approved release, immediately before merging this branch into `master`; verify the deployment workflow succeeds and check the live homepage, experience, one old and one new article, agent downloads, custom-domain HTTPS, and 404. Retain the previous commit as the rollback point. Local/branch CI success does not demonstrate a completed live deployment.

Limits: the visual/browser audit uses Chromium, not a full Safari/Firefox or assistive-technology matrix. External services and archived sources can change independently. The existing 2024 CTO period and April 2022–2023 lead-developer period are retained as supplied; no intervening dates were inferred.


### Agent prompt URL regression

The generic static server previously used for port 4175 served a production build. Its clickable download links resolved locally, but absolute URLs inside the prompt and downloads pointed at the public domain, where the new files do not exist until release. The active preview now uses `./scripts/serve --port 4175 --destination /tmp/mario-site-preview`; development-mode URLs use the actual preview port throughout. Production builds retain canonical HTTPS endpoints.

`scripts/check-agent-links.py` follows all internal agent-screen links, three prompt URLs, four exports, and all eight article/Markdown pairs over HTTP (28 unique local URLs). It verifies plain-text downloads, JSON, export titles, and prompt copy behavior. `./scripts/check` now also verifies the URLs embedded in the prompt against the build configuration and confirms each referenced file exists. The HTTP check must use a development preview before deployment, or the real public domain after deployment.
