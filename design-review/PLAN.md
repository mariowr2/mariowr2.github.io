# Current implementation entry point

**The selected design is Thin Ridgeline / A Measured Ascent.** Read [HANDOFF.md](HANDOFF.md) and [selected.json](selected.json) to implement it. The mountain is optional and expected to be replaceable with a personal photograph; the original headshot stays independently. The branch is `redesign/thin-ridgeline`. Earlier exploration and recommendations below are historical context, not a request for another design round.

---

# Dark revision: blog, experience, and an agent handoff

**Latest exploration:** A Measured Ascent was selected. The next [three low mountain marks](mountains.html) keep that layout and portrait, remove the ascent cues, and make the subtle motion occur while the shallow graphic remains visible. See [MOUNTAINS.md](MOUNTAINS.md).

**Previous exploration:** High Pass was selected, with a request for quieter, less literal motion and preservation of the original portrait. See [three quieter ascents](quiet.html) and [QUIET.md](QUIET.md): an abstract incline, a small Sisyphus detail, and a cairn, with three different photo placements.

**Previous exploration:** six [main/header animation pairings](pairings.html) extend the selected floating-header design. Each has original main artwork, a different header companion, and a quiet “Agent version” tab. Details: [PAIRINGS.md](PAIRINGS.md).

**Previous exploration:** Still Climbing was selected from the personal variants. See [three live scroll studies](motion.html) and [their implementation notes](SCROLL.md) for a margin bike, a climbing companion in the masthead, and a reading trail.

**Previous exploration:** the blog was selected. See [four personal variations](personal.html) and [their design notes](PERSONAL.md) for the next review: cats, bicycles, mountains, and endurance sports. Two preserve the selected blog's copy and sections; two revise them.

October 28, 2026. This replaces the first cream/serif exploration. The user liked the structure, rejected the palettes, fonts, and tone, and asked to retain the original site's darkness with readable green and terminal-like type. The agent version should be obvious to human visitors.

## Review the layouts

Open [the comparison](index.html). All three directions now use a dark background, off-white text, and green links. The differences are about reading, density, and how the writing is organized:

| Layout | Type | Structure |
| --- | --- | --- |
| [The blog](journal/index.html) | IBM Plex Mono throughout | Brief personal introduction, recent writing, older writing, small work sidebar |
| [Notes by topic](fieldguide/index.html) | IBM Plex Mono throughout | Compact archive with working subject filters; headings carry more green |
| [Work & writing](record/index.html) | Mono navigation, Plex Sans long text | Dated experience linked to related posts; a more familiar long-form reading alternative |

Each includes all eight real article bodies and the thirteen existing professional timeline entries. Homepage descriptions and summaries are proposed copy; the source articles are unchanged. No fake projects, placeholder metrics, or fictional notes were added.

My current recommendation is the blog layout. Compare its full article view with Work & writing before choosing mono for long reading. Keep the useful archive and experience structure; avoid adding decorative terminal commands or simulated desktop windows.

## Design guidance

I looked up and applied [Anthropic's frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). It was read for this task, not installed globally. Specific design tokens, typography, wireframe, and critique are recorded in [DESIGN.md](DESIGN.md).

The self-hosted [IBM Plex](https://github.com/IBM/plex) Mono and Sans files come from Google Fonts' distribution. Their OFL licenses are included under `assets/fonts/`. They work without contacting a font service. Text is static and selectable; navigation is ordinary links. The original oversized image and timeline line are not used.

[Initial research](RESEARCH.md) includes the Fowler, Evans, Appleton, Willison, HTML-in-Canvas, and agent-discovery references. The initial palettes and slogans are superseded, not recommendations to bring back.

## Make agent support visible

The request is both a useful representation for agents and a visible sign to humans that the site was built with those readers in mind.

- A green **For agents** link appears in the main navigation.
- The homepage has a green-framed **Send your agent here** panel with a prominent briefing link and direct Markdown/JSON links.
- At phone widths a compact handoff link appears before the writing list, so agent access does not depend on reaching the sidebar below the archive.
- The [dedicated agent page](agents/index.html) explains the purpose in ordinary language and supplies a working copyable prompt. It falls back to selecting the text when clipboard access is unavailable.
- [profile.md](profile.md), [profile.json](profile.json), [writing.md](writing.md), [llms.txt](llms.txt), and eight article Markdown files are available as actual files, not promised future buttons.
- The prompt asks the agent to cite source material and to distinguish Mario's own words from interpretation. It does not invent current title dates.

These are local review files. They must be attached to an agent conversation or served where the agent can reach them. A local `file://` link is not accessible to someone else's remote agent. The page explicitly says the proposed public root endpoints are not deployed. Once the design is selected, the public handoff should provide one stable HTTPS URL and a prompt using that URL instead of attachments.

## Production implementation after selection

1. **Confirm the public profile.** Agree on current role wording, known dates, public contact details, and preferred first-person introduction. Extract shared profile/history fields into `_data/profile.yml`.
2. **Implement the chosen Jekyll layout.** Replace old presentation dependencies only when templates stop using them. Keep typography, palette, and density from the selected prototype. Maintain the visible agent link and panel.
3. **Preserve the record.** Retain every current post URL and the existing feed/archive. Build a compact `/experience/` page and link it to relevant posts. Review legacy copied HTML/embeds without silently deleting content.
4. **Publish the same data twice.** Render human pages and machine-readable files from the same sources: `/for-agents/`, `/profile.md`, `/profile.json`, `/writing.md`, `/llms.txt`, and per-article Markdown alternates. Generate ProfilePage/Person and BlogPosting JSON-LD where appropriate. Do not maintain a separate embellished agent biography.
5. **Verify the handoff.** Fetch the files over actual public HTTPS, follow the prompt with an agent, and check citations against the original pages. Validate JSON, Markdown discovery, feed and sitemap. A public read-only record does not require an MCP server.
6. **Validate and release.** Compare old/new route manifests; test mobile reading, keyboard access, no-JavaScript navigation, contrast, and the clipboard fallback. Confirm GitHub Pages settings before deployment.

The site's core remains semantic HTML/CSS. The recent Google HTML-in-Canvas API is not needed for this redesign. A future experiment can use it with a fallback if there is a real interactive use case.

## Reviewing and regenerating

Open `index.html` directly in a browser, or run this from the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Then visit http://127.0.0.1:4173/design-review/ . Run `./scripts/render-designs` after editing the prototype templates or changing the posts/timeline. It builds Jekyll and regenerates the layouts, agent page, readable profile, JSON, writing index, and Markdown posts. The shared ERB templates and CSS are the source for generated HTML.

The review folder remains excluded from production builds. It is not the deployed site. [QA.md](QA.md) records browser checks, limits, and screenshot regeneration commands. [README.md](../README.md) describes the repository setup.
