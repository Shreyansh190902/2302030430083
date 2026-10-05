# @_risewithsk carousel templates

Instagram carousels (1080×1350, 4:5) for the @_risewithsk motivation page.

| Template | Style | Output |
|---|---|---|
| `template.html` | Bold: black + gold, Anton headlines | `slide-N.png` |
| `minimal.html` | Minimal editorial: light grey grid, Playfair Display serif + Inter | `minimal-N.png` |

Edit the text inside each `<section class="slide">`, then render:

    NODE_PATH=$(npm root -g) node risewithsk-carousel/render.js                      # bold
    NODE_PATH=$(npm root -g) node risewithsk-carousel/render.js minimal.html minimal # minimal

In `minimal.html`, replace `SK` inside `.avatar` with `<img src="photo.jpg">` to use a real profile photo.
Fonts live in `fonts/` so rendering works offline.
