# @_risewithsk carousel templates

Instagram carousels (1080x1350, 4:5) for the @_risewithsk motivation page.

**Chosen theme: Notebook** (`notebook.html` + `notebook.css`): handwritten notes on
lined paper, yellow marker highlight, red circled note, hand-drawn checkboxes.

Edit the `POSTS` list in `notebook.html` (`*word*` = marker highlight, `|` = line
break, `note` = red circle), then render:

    NODE_PATH=$(npm root -g) node risewithsk-carousel/render.js notebook.html

Output: `posts/notebook/<carousel>/slide-N.png`. Captions: `posts/CAPTIONS.md`.

Earlier explorations (not used): `template.html` (bold), `minimal.html` /
`posts.html` (minimal grid), `sunrise.html`, `themes.html` (neon / notebook / royal).
Fonts live in `fonts/` so rendering works offline.
