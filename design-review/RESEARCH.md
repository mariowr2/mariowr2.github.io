# Initial research — archived direction

The initial light palettes and editorial names below were rejected in review. See [the current plan](PLAN.md) and [design decisions](DESIGN.md) for the dark revision. Reference research and migration considerations remain useful.

# A public record of a curious builder

Design research and prototype plan · October 28, 2026

## The brief

Mario is a 28-year-old CTO and founder who loves coding, systems, products, learning, experiments, and building teams. This website should make that person legible through his actual work and thinking. The primary product is a useful, growing public record: writing someone can learn from, a professional history someone can understand, and source material an agent can reliably retrieve.

Success means a first-time reader can answer: Who is Mario? What does he think about? What has he built? What can I learn here? How do I reach him? A returning reader should get to new writing immediately.

The current fullscreen image, oversized spacing, alternating timeline, uppercase typography, and animation-heavy theme put presentation ahead of those answers. Replace that visual hierarchy with a short introduction, visible writing, compact context, and comfortable article typography. Keep breathing room around text without requiring scrolling through empty sections.

## Research and what it changes

These are design interpretations of first-party sites, not claims that the authors endorse this work. Sources accessed October 28, 2026.

| Reference | Observed pattern | Application to Mario |
| --- | --- | --- |
| [Martin Fowler](https://martinfowler.com/) | An enduring library organized around software practices and topics, with author context and feeds. | Build an archive that stays useful beyond its publish date. Take the editorial clarity rather than copying the full navigation or visual identity. |
| [Julia Evans](https://jvns.ca/) | A welcoming introduction, recent writing, and an extensive archive by subject. | Make learning in public feel approachable. Readers should see real writing immediately. |
| [Maggie Appleton](https://maggieappleton.com/) | Distinguishes essays, notes, and a growing garden of ideas. | Give unfinished thinking a truthful home separate from polished essays. Add these formats when content exists. |
| [Simon Willison](https://simonwillison.net/) | Essays, links, notes, and tools coexist in a dated publication. | Lower the effort of recording a learning or experiment without requiring every update to become a long essay. |

### The Google reference

The strongest match is [Chrome’s HTML-in-Canvas announcement](https://developer.chrome.com/blog/html-in-canvas), published **October 26, 2026**, two days before this review. It describes rendering DOM elements in canvas while retaining browser integrations, including text selection and accessibility. The article identifies Chrome 157 and supplies feature-detection and fallback guidance. This is distinct from [Gemini Canvas](https://blog.google/products-and-platforms/products/gemini/gemini-collaboration-features/), the HTML/React prototyping workspace introduced in March 2025.

Recommendation: ordinary semantic HTML and CSS for the site. HTML-in-Canvas could be an optional experiment inside a future article that genuinely benefits from a visual simulation. Its documentation is not evidence of cross-browser support. Keep a visible HTML explanation and functional fallback; feature-detect before enabling it. The current prototypes intentionally demonstrate the concept map using ordinary SVG. They do not implement or claim to test the new API.

## Three directions

### 01 · The Working Journal

**Promise:** “Here is what I’m learning while building.”

A warm editorial website, with cream paper, dark brown text, restrained terracotta links, serif headlines, and sans-serif interface text. The homepage leads with a compact personal introduction and two recent essays. A sidebar supplies just enough career context and human voice. Earlier writing appears as a list, without a card for every item.

- Home: recent writing → earlier chapters, supported by a compact biography and experience summary.
- Reading: a narrow text column, quiet publication metadata, original post body, and a route to the professional story.
- Experience: one-column chronological entries with dates, short descriptions, and relevant essays attached to the work.
- Signature: the site feels like an ongoing correspondence from a practitioner. Personal language and a consistent editorial rhythm create identity.
- Strength: strongest fit for the current eight-post library; least publishing overhead and smallest implementation scope.
- Tradeoff: topics and experiments may be harder to discover as the archive grows. Add topic pages without expanding homepage navigation prematurely.
- Scope after selection: replace shared layout, stylesheet, homepage/archive, post layout, and timeline presentation. Keep all current post routes.

**Choose it if:** people should remember the writing and your voice first.

### 02 · The Field Guide

**Promise:** “Here is how my understanding connects across software, products, and people.”

A crisp, pale-sage interface with forest accents, clear sans-serif typography, small monospaced labels, and a compact learning-loop diagram. This is a collection of useful ideas, not a dashboard. Subject filters provide multiple ways into the actual archive. Questions for future writing are explicitly labelled as prompts.

- Home: topic filters → published entries, accompanied by a small model of the connections between subjects.
- Reading: direct, technical typography with a clear connection back to the library and career context.
- Experience: the same factual history, framed as the origin of the knowledge.
- Signature: relationships between systems, teams, products, and experiments. A future topic landing page can answer a question and collect the relevant essays, rather than just list tags.
- Strength: best fit for systems thinking, team topologies, communication, and experimenting with emerging technologies.
- Tradeoff: eight posts are not yet a large knowledge base. Avoid empty topics, invented notes, or speculative “recent experiments.” Subject assignments in this prototype are editorial suggestions.
- Scope after selection: shared redesign plus a small curated topic data model, topic landing pages, note/essay distinction, and optional related-reading metadata. Search can wait until the archive warrants it.

**Choose it if:** the site should become a body of knowledge that readers explore by interest.

### 03 · The Build Record

**Promise:** “Here is what I worked on, what happened, and what I learned.”

A cool off-white and blue publication, with a small monospaced masthead, compact date markers, and strong sans-serif chapter headings. The homepage links three existing essays to professional chapters: the seed round, the MVP launch, and robot music. No giant central line or alternating milestone bubbles.

- Home: selected chronological chapters → remaining archive, with a compact “current chapter” note.
- Reading: essay plus routes to the associated work and professional history.
- Experience: precise chronological entries, including overlapping activities rather than forcing everything into one linear job sequence.
- Signature: the relationship between work and reflection. A professional record supported by evidence rather than a generic résumé or a list of technology logos.
- Strength: strongest for someone trying to understand your trajectory as a founder and technical leader.
- Tradeoff: chronology may obscure evergreen ideas, and infrequent long posts can make the homepage look inactive. Show dates honestly; introduce short updates only when you actually want to publish them.
- Scope after selection: shared redesign plus structured experience data and explicit links between roles, projects, and writing.

**Choose it if:** the professional story should be the primary way people understand your thinking.

## Recommendation

Start with **the Working Journal**, add **the Field Guide’s topic trails** as writing accumulates, and use **the Build Record’s connection between experience and lessons** on the history page. This is a focused starting point that still supports a much richer long-term record.

Do not merge every feature onto the homepage. Choose one dominant hierarchy. The decision here is which invitation feels most like Mario: read what I’m learning, explore how I think, or follow the work.

## Shared information architecture

Proposed production routes, not all implemented in this review:

| Route | Purpose |
| --- | --- |
| `/` | Introduction, recent or selected writing, compact current context |
| `/blog/` | Complete writing archive; preserve existing address |
| Existing dated post routes | Full essays; retain every current route |
| `/experience/` | Professional history with related writing/projects |
| `/about/` | Durable biography, interests, current role, contact, and profile links |
| `/topics/<slug>/` | Add selectively for subjects with enough writing |
| `/notes/` | Optional later; brief learnings, experiments, and evolving thinking |
| `/feed.xml`, `/sitemap.xml` | Existing feed and URL discovery, maintained through migration |
| `/llms.txt`, `/profile.json`, article Markdown alternates | Public, first-party agent access |

Keep navigation to Writing, Experience, and About/contact initially. The prototype uses Writing, Experience, and Say hello. A “now” page is optional; avoid creating an update obligation before deciding whether you want one.

## Agents as first-party readers

Agent support starts with the same readable, static HTML humans receive. It should not depend on a chat widget or browser-only interactions.

1. **One source of truth.** Move public professional data into a Jekyll data file, such as `_data/profile.yml`. Render the experience page, biography summary, structured data, and JSON export from it. Use explicit start/end dates only when known; preserve the uncertainty and overlaps in the existing timeline.
2. **Discoverable exports.** Publish a concise `/llms.txt` with canonical links to biography, experience, writing index, and Markdown articles. [llms.txt](https://llmstxt.org/) remains a proposal/discovery convention, not a guarantee of ingestion, ranking, or crawler permission.
3. **Per-page representation.** Generate a Markdown alternate for each article from the same source and expose it with `rel="alternate" type="text/markdown"`. Resolve Liquid substitutions. Include title, publication/update dates, author, canonical URL, and references. Preserve meaningful embedded content with descriptive links where needed.
4. **Structured identity.** Use [Schema.org ProfilePage](https://schema.org/ProfilePage) with `mainEntity: Person` on About and `BlogPosting` on articles. Stable identifiers tie author and posts together. Include only verifiable role titles, affiliation, profile links, and dates; do not invent an exact CTO start date from the existing “2024–present” wording.
5. **Citable records.** JSON entries include stable IDs, canonical URLs, dates, descriptions, provenance, and a schema version. Distinguish the original publish date from a genuine substantive update. Do not imply that a rebuild means the content was reviewed.
6. **A simple read surface.** No MCP server is needed for public static content. If useful interactive tools appear later, assess a narrow tool interface then. A public profile does not need an agent to log in or execute JavaScript.
7. **Honest constraints.** Machine-readable content is as public as the HTML. Export only intended public material. `robots.txt` governs crawler preferences separately; llms.txt does not control access.

This review demonstrates `design-review/llms.txt`, `profile.json`, and eight Markdown article exports. Article pages link their Markdown alternate; all pages link the structured record. These are explicitly marked prototype data. Production root endpoints, JSON-LD, and an integrated Jekyll export pipeline are next-phase work.

## Content and identity decisions

- Use “CTO and founder” from the user’s brief, but verify the exact employer/title phrasing and dates before publishing a detailed biography.
- Do not hard-code age into the public biography: it becomes stale and adds little to the professional story.
- Retain the strong personal language already present: “Always a work in progress,” curiosity, the MVP mindset, and learning to build a team you want to be part of.
- Proposed homepage copy and article summaries are editorial drafts. Full article bodies come from the built repository; the existing post source is unchanged.
- History descriptions are sourced from `_config.yml`. Display headings are compact editorial summaries. A 2024 entry is deliberately titled “Building Evotrux,” not assigned an unverified promotion or founding date.
- Do not fill empty categories with generated essays or fictitious projects. Future prompts are labelled as such.
- Keep project images where they explain the work, within articles or small context areas. Avoid a stock-photo hero, decorative portrait wall, or unnecessary generated images.

## Implementation plan after choosing a direction

### 1. Establish the public content model

Inventory current URLs and save a route manifest. Extract timeline/profile data into `_data/`. Confirm current role naming, preferred biography/contact details, and whether a headshot adds value. Decide whether notes are a real publishing commitment. Keep current Markdown posts and their URLs.

### 2. Build a coherent Jekyll theme

Create the chosen shared document layout, navigation, footer, tokens, and responsive styles. Replace Bootstrap/jQuery presentation with native HTML/CSS and tiny optional JavaScript where useful. Move old theme assets out only after no live templates depend on them. Retain original licensing attribution where required.

### 3. Migrate writing and experience

Build homepage, archive, reading template, and history. Add stable in-page headings, topic links, and links from roles/projects to related articles. Review legacy pasted HTML, mixed-content media, oversized iframes, sharing snippets, and old comment links individually without silently deleting article content. Revisit inherited analytics separately.

### 4. Add machine-readable publishing

Generate profile JSON, llms.txt, Markdown alternates, and JSON-LD from the same data/content as the HTML. Keep the feed and sitemap accurate. Validate exports and ensure agent content does not drift from visible content.

### 5. Verify and release

Run existing build/link checks and a before/after route comparison. Validate keyboard use, focus, contrast, mobile layout, long titles, full article embeds, no-JavaScript reading, and feed/XML/JSON output. Aim for no third-party runtime dependency for core navigation or typography. Check rendered desktop/mobile pages and actual hosting settings before changing deployment. Publish the selected design only after reviewing the real pages.

## Evaluation session

Open `index.html` in this directory or serve the repo using:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Then visit http://127.0.0.1:4173/design-review/ . These are standalone HTML artifacts and do not require the Jekyll development server. Start it in a separate terminal from the repository root. Root-relative legacy article media is resolved to the current public domain; existing third-party embeds still require network access. Site typography, layout, and navigation require no external fonts or libraries. Existing history images use the local `img/` assets.

For each direction, try the homepage, reading view, and history page at desktop and phone widths. Use the actual long post, not just the top of its first screen. All eight article links have a matching reading view. Field Guide filters are functional and optional; no-JavaScript browsing shows every article.

Score 1–5:

| Criterion | What to look for |
| --- | --- |
| Feels like me | Curious builder and leader, with enough warmth and personality |
| Clarity | Who I am and what this site offers are clear in seconds |
| Reading | Comfortable for a substantial article on phone and desktop |
| Discovery | Can find both new writing and older relevant ideas |
| Professional record | Experience is precise, compact, and connected to actual work |
| Publishing fit | I would enjoy adding to this for years |
| Agent access | A reader can retrieve facts and source text without running the UI |

My provisional ranking: Journal for the initial release, Field Guide for the long-term knowledge structure, Build Record for the experience narrative. This is a design recommendation, not user testing evidence.

## Files and verification

- `index.html`: comparison gallery and direct links.
- `journal/`, `fieldguide/`, `record/`: ten HTML pages per direction (home, history, eight articles).
- `assets/`: shared styles, tiny filter script, desktop/mobile home captures, and reading captures.
- `templates/page.erb`: shared prototype markup with distinct home structures and theme tokens.
- `text/`, `profile.json`, `llms.txt`: review-only machine-readable representations.
- `../scripts/render-designs`: regenerate content from the current repository, including a production build first. Requires the existing Bundler dependencies; no Node dependency is added.

`design-review/` is excluded from Jekyll output, so these review artifacts do not become production pages through a normal build. Production homepage/templates are unchanged. These prototype files have noindex metadata as an additional guard if served elsewhere. Do not publish them as the new public site by accident.

Browser QA and final validation results are recorded in `QA.md`. Selection and implementation remain separate: this delivery is a reviewable design exploration, not a deployed redesign.
