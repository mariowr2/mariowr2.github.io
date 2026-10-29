# Personal variations on the selected blog

The selected foundation is the dark blog: Plex Mono, off-white reading text, soft green links, real writing, and visible agent access. The new brief adds cats, bicycles, marathon running, multi-day bike trips, and mountains as a symbol of patient growth and testing limits.

The follow-up removes the restriction on copy changes. This review therefore contains four variations: two restrained additions preserving the selected homepage's text and sections, and two freer alternatives with proposed personal copy and adjusted composition.

| Option | Scope | Distinguishing element |
| --- | --- | --- |
| [A cat in the margins](cat/index.html) | Original homepage copy and sections preserved | A hand-drawn cat in a window; wake it and its eyes follow the pointer |
| [The long route](ride/index.html) | Original homepage copy and sections preserved | A bicycle following an illustrated mountain route; scrub its position |
| [Still climbing](summit/index.html) | Personal introduction and sidebar copy; existing writing/history retained | Contour lines and a trail; move a hiker a step at a time |
| [Field notes](notebook/index.html) | More personal introduction, writing-first main column, personal sidebar | Three small illustrated interests, a responsive cycling sketch, and compact writing |

All illustrations are code-native SVG, drawn for this review. No emojis, generated stock illustrations, tracking, or external image/font services are introduced. Routes and mountain forms are illustrative, not GPS traces or claims about a specific climb. No race times, event names, distances, bike specifications, or owned pets are invented.

Interactions are optional. The illustrations remain visible with JavaScript off; reading and agent access use ordinary links. Keyboard controls have labels, motion is user initiated, and reduced-motion users get immediate position changes. Text stays selectable and the visual details sit outside the article body.

The baseline blog remains at `journal/`. New variants use its templates/styles and have full article/history views, preserving the public-record functions. Their homepage introductions and personal descriptions in the last two are editorial drafts for review, not changes to source posts or the production biography. The first two preserve `.intro`, writing, and sidebar content exactly, apart from the added illustration controls.

Review at [personal.html](personal.html). Sources are `templates/personal-scene.erb`, `templates/notebook.erb`, `assets/personal.css`, `assets/personal.js`, and the existing prototype renderer. Regenerate with `./scripts/render-designs`. Capture/check scripts are under `scripts/`; screenshots are under `assets/`. These artifacts remain excluded from the Jekyll production site.

My recommendation: compare the cat option's restraint with the mountain option's more personal copy. The mountain fits the endurance and slow-growth idea; the cat makes the technical setting feel inhabited. A final version could borrow one small detail from the other without combining every illustration on the homepage.
