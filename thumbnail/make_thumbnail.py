"""Generate the YouTube thumbnail for the "Kamal Chhe Tu Kaku" star-cast episode.

Background: cast-group.webp (4 cast members on the magenta stage). The real
film logo is keyed out of poster.webp and placed above the cast.

Usage: python3 make_thumbnail.py  ->  writes thumbnail.png / thumbnail.jpg (1280x720)
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
W, H = 1280, 720

GOLD = (255, 205, 40)
WHITE = (255, 255, 255)
INK = (24, 4, 30)
RED = (230, 20, 60)

ANTON = str(HERE / "fonts/Anton-Regular.ttf")
POPPINS = str(HERE / "fonts/Poppins-Black.ttf")
GUJ = str(HERE / "fonts/HindVadodara-Bold.ttf")



def font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def load_background():
    return Image.open(HERE / "cast-group.webp").convert("RGB").resize((W, H), Image.LANCZOS)


def keyed_logo():
    """Cut the Gujarati title art out of the poster's magenta background."""
    poster = Image.open(HERE / "poster.webp").convert("RGB")
    p = np.asarray(poster).astype(float)
    r, g, b = p[..., 0], p[..., 1], p[..., 2]
    fg = (g > 85) | (b > r * 1.02)  # white/gold letters or purple extrusion
    alpha = np.where(fg, 255, 0).astype("uint8")
    ph, pw = alpha.shape
    alpha[:, int(pw * 0.80):] = 0  # flying cash props
    alpha[int(ph * 0.83):, : int(pw * 0.45)] = 0  # director credit + swirl
    alpha[int(ph * 0.90):, : int(pw * 0.49)] = 0  # tail of "SATYAM RAJ"
    alpha[:8, :] = 0  # border line
    a = Image.fromarray(alpha).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1))
    logo = poster.convert("RGBA")
    logo.putalpha(a)
    return logo.crop(logo.getbbox())


def shadowed(canvas, draw_fn, blur=6, offset=(5, 6), opacity=180):
    """Run draw_fn(draw, fill_override) once as a soft shadow, then for real."""
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(shadow), (0, 0, 0, opacity), offset)
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
    draw_fn(ImageDraw.Draw(canvas), None, (0, 0))


def text_block(canvas, xy, text, fnt, fill, stroke=0, anchor="la"):
    def draw(d, shade, off):
        d.text(
            (xy[0] + off[0], xy[1] + off[1]), text, font=fnt, fill=shade or fill,
            stroke_width=stroke, stroke_fill=shade or INK, anchor=anchor,
        )
    shadowed(canvas, draw)


def tag(canvas, xy, text, fnt, bg, fg, angle=0, pad=(26, 16)):
    tb = ImageDraw.Draw(canvas).textbbox((0, 0), text, font=fnt)
    box = Image.new("RGBA", (tb[2] - tb[0] + pad[0] * 2, tb[3] - tb[1] + pad[1] * 2), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 0, box.width - 1, box.height - 1), radius=14, fill=bg)
    bd.text((box.width / 2, box.height / 2), text, font=fnt, fill=fg, anchor="mm")
    box = box.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 170), (xy[0] + 6, xy[1] + 7), box.getchannel("A"))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    canvas.alpha_composite(box, xy)


def main():
    canvas = load_background().convert("RGBA")

    # --- Centre top: the real film logo, sitting just above the heads ---
    logo = keyed_logo()
    logo_h = 272
    logo = logo.resize((int(logo.width * logo_h / logo.height), logo_h), Image.LANCZOS)
    lx, ly = (W - logo.width) // 2 + 4, 4
    canvas.alpha_composite(logo, (lx, ly))

    # --- Top left: STAR CAST / UNFILTERED! ---
    text_block(canvas, (34, 18), "STAR CAST", font(ANTON, 96), GOLD, stroke=5)
    tag(canvas, (30, 140), "UNFILTERED!", font(ANTON, 58), RED, WHITE, angle=4)

    # --- Top right: English title + exclusive badge ---
    bf = font(POPPINS, 24)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((W - 236, 22, W - 30, 68), radius=23, fill=GOLD)
    d.ellipse((W - 216, 36, W - 198, 54), fill=RED)
    d.text((W - 122, 46), "EXCLUSIVE", font=bf, fill=INK, anchor="mm")
    tf = font(POPPINS, 44)
    text_block(canvas, (W - 30, 84), "KAMAL CHHE TU", tf, WHITE, stroke=4, anchor="ra")
    text_block(canvas, (W - 30, 136), "KAKU", font(POPPINS, 60), GOLD, stroke=5, anchor="ra")

    # --- Bottom centre: Gujarati tagline pill ---
    gf = font(GUJ, 44)
    guj = "ફિલ્મની વાતો • મસ્તી • ધમાલ"
    gb = d.textbbox((0, 0), guj, font=gf)
    gw = gb[2] - gb[0]
    cy = H - 52
    x0, x1 = (W - gw) / 2 - 34, (W + gw) / 2 + 34

    def pill(dd, shade, off):
        dd.rounded_rectangle(
            (x0 + off[0], cy - 36 + off[1], x1 + off[0], cy + 38 + off[1]), radius=38,
            fill=shade or INK, outline=shade or GOLD, width=4,
        )
    shadowed(canvas, pill, blur=10, opacity=200)
    ImageDraw.Draw(canvas).text((W / 2, cy + 2), guj, font=gf, fill=WHITE, anchor="mm")

    canvas.convert("RGB").save(HERE / "thumbnail.png", optimize=True)
    canvas.convert("RGB").save(HERE / "thumbnail.jpg", quality=92)
    print("wrote thumbnail.png / thumbnail.jpg")


if __name__ == "__main__":
    main()
