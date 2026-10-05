# @_risewithsk carousel template

Instagram carousel (1080×1350, 4:5) for the @_risewithsk motivation page.

- `template.html` – all slides; edit the text inside each `<section class="slide">`.
- `render.js` – exports every slide to `slide-N.png`.
- `fonts/` – Anton (headlines) and Poppins (body), loaded locally.

Render:

    NODE_PATH=$(npm root -g) node risewithsk-carousel/render.js
