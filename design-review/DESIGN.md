# Revision: dark, direct, visibly built for agents

The user prefers the previous site's black background and white text, wants readable green and terminal-like typography, and rejected the initial palettes, fonts, and tone. Keep the useful writing/history structure. Make agent access obvious to people as well as useful to software.

## Design skill

Applied [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), fetched October 28, 2026. The relevant process is to choose a subject-specific visual direction, make type and copy intentional, and critique the result before implementation. Read remotely for this task; not installed globally. This repository's instructions and the user's preferences take precedence.

Additional type reference: [IBM Plex](https://github.com/IBM/plex), an open-source family with Mono and Sans companions. Local font files are unmodified Google Fonts distributions; OFL licenses accompany them.

## Tokens

| Role | Blog / journal | Topic index | Work & writing |
| --- | --- | --- | --- |
| Background | `#080b09` | `#080b09` | `#080a09` |
| Raised surface | `#101912` | `#0e1711` | `#111713` |
| Reading text | `#e5e9e4` | `#e2ebe1` | `#e8ebe7` |
| Secondary text | `#a4b0a3` | `#a3b4a2` | `#a9b3a7` |
| Link / accent | `#9cce8b` | `#a5d69b` | `#a2c992` |
| Rule | `#2a352b` | `#2c392d` | `#2a352b` |

IBM Plex Mono regular/medium provides the blog and topic index's actual body and heading typography, not just tiny decorative metadata. IBM Plex Sans provides an alternative for long reading in Work & writing. A self-hosted font avoids CDN requests and keeps the face consistent when opening the HTML artifact directly. Main reading remains off-white. Green carries links, selected topics, and the agent panel. No glow or continuous animation.

## Structure

Keep text left aligned. Use a small masthead, a factual first-person introduction, a reading list, and a narrower sidebar. Make the agent handoff a real navigable destination. Dates, topics, and file-format labels identify actual information.

```text
Mario Mendez       Writing / Experience / For agents / Email

Hi, I'm Mario.                 [or: Writing / Work & writing]
CTO, founder. [brief introduction in ordinary words]

Recent writing                 Give your agent a starting point
Date, title, short summary      Read the briefing / Markdown / JSON
Date, title, short summary
                               About / selected experience
Older writing                  Contact
```

The three variants now test density and typography within the user's preferred dark identity, not unrelated brand directions. A common agent page provides the exact files plus a selectable briefing prompt. It explains the representation in human terms rather than exposing implementation details throughout the reading UI.

## Critique before implementation

The first exploration leaned on cream paper, serif display, all-caps labels, arrows, and broad slogans. Those choices were not specific to Mario. Replace the display slogans with simple page headings, sentence-case labels, direct summaries, and material from his posts. Remove the conceptual diagram and speculative writing prompts: published experience says more than a generic map of interests.

Dark green can itself become a stock developer aesthetic. Here its basis is the user's existing preference, and its use is bounded: familiar web navigation, no command syntax required, no simulated boot sequence, no fake code, no decorative line numbers, no Matrix effects. The human-facing agent handoff is the distinctive useful feature.

## Copy rules

Say “Writing,” “Experience,” and “For agents.” Introduce Mario as a person. Preserve the actual article titles and original body text. Summaries describe what happened. Don't add grand claims or aphorisms. Keep proposed copy and role-date uncertainty documented in the plan rather than filling the public-facing UI with review notes.

## Agent handoff

The user explicitly wants people to notice that an agent version exists. Put it in primary navigation and a green-framed homepage panel near the first writing entries. The dedicated page explains what an agent can retrieve, provides a copyable prompt, and links the profile JSON, readable profile, Markdown writing index, and individual articles. State clearly that this is a local review copy and root production endpoints are not live yet.
