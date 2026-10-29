"""Generate the YouTube thumbnail for the "Kamal Chhe Tu Kaku" star-cast episode.

Usage: python3 make_thumbnail.py  ->  writes thumbnail.png (1280x720)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).parent
W, H = 1280, 720

# Brand palette (pulled from the film poster)
MAGENTA = (176, 24, 140)
PLUM = (58, 8, 70)
GOLD = (255, 205, 40)
WHITE = (255, 255, 255)
INK = (24, 4, 30)

ANTON = str(HERE / "fonts/Anton-Regular.ttf")
POPPINS = str(HERE / "fonts/Poppins-Black.ttf")
GUJ = str(HERE / "fonts/HindVadodara-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def gradient_bg():
    """Diagonal plum -> magenta gradient with a soft glow behind the title."""
    bg = Image.new("RGB", (W, H))
    px = bg.load()
    for y in range(H):
        for x in range(W):
            t = min(1, max(0, (x * 0.6 + y * 0.4) / (W * 0.75)))
            px[x, y] = tuple(int(PLUM[i] + (MAGENTA[i] - PLUM[i]) * (1 - t)) for i in range(3))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-200, -150, 700, 450), fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    bg.paste(Image.new("RGB", (W, H), (255, 90, 200)), mask=glow)
    return bg


def cover(img, size, focus=(0.5, 0.5)):
    return ImageOps.fit(img, size, Image.LANCZOS, centering=focus)


def shadow_text(draw_img, xy, text, fnt, fill, stroke=0, stroke_fill=INK, offset=6, anchor="la"):
    """Text with a hard drop shadow and optional outline."""
    shadow = Image.new("RGBA", draw_img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text(
        (xy[0] + offset, xy[1] + offset), text, font=fnt, fill=(0, 0, 0, 170),
        stroke_width=stroke, stroke_fill=(0, 0, 0, 170), anchor=anchor,
    )
    draw_img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(draw_img).text(
        xy, text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor=anchor,
    )


def main():
    canvas = gradient_bg().convert("RGBA")

    # --- Right side: the two cast photos stacked, cut by a diagonal edge ---
    cast1 = Image.open(HERE / "cast-1.jpg").convert("RGB")
    cast2 = Image.open(HERE / "cast-2.jpg").convert("RGB")
    panel_w = 700
    top = cover(cast1, (panel_w, H // 2), focus=(0.5, 0.35))
    bottom = cover(cast2, (panel_w, H // 2), focus=(0.5, 0.4))
    photos = Image.new("RGB", (panel_w, H))
    photos.paste(top, (0, 0))
    photos.paste(bottom, (0, H // 2))

    x0 = W - panel_w
    slant = 140
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(x0 + slant, 0), (W, 0), (W, H), (x0, H)], fill=255)
    layer = Image.new("RGBA", (W, H))
    layer.paste(photos, (x0, 0))
    canvas.paste(layer, (0, 0), mask)

    d = ImageDraw.Draw(canvas)
    # Gold divider between photos and along the diagonal
    d.line([(x0 + slant * 0.5, H // 2), (W, H // 2)], fill=GOLD, width=8)
    d.line([(x0 + slant, 0), (x0, H)], fill=GOLD, width=14)
    d.line([(x0 + slant + 16, 0), (x0 + 16, H)], fill=WHITE, width=4)

    # --- Top-left: the film's Gujarati logo, cropped from the poster ---
    poster = Image.open(HERE / "poster.webp").convert("RGBA")
    pw, ph = poster.size
    logo = poster.crop((int(pw * 0.05), int(ph * 0.02), int(pw * 0.82), ph))
    logo_w = 470
    logo = logo.resize((logo_w, int(logo.height * logo_w / logo.width)), Image.LANCZOS)
    # Feather the edges so the poster background melts into ours
    fade = Image.new("L", logo.size, 0)
    ImageDraw.Draw(fade).rounded_rectangle((30, 20, logo.width - 30, logo.height - 30), radius=60, fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(22))
    canvas.paste(logo, (30, -6), fade)

    # --- English title line ---
    shadow_text(canvas, (44, 352), "KAMAL CHHE TU KAKU", font(POPPINS, 38), WHITE, stroke=3)

    # --- STAR CAST UNFILTERED! banner ---
    banner_font = font(ANTON, 90)
    text = "STAR CAST"
    shadow_text(canvas, (40, 392), text, banner_font, GOLD, stroke=5)
    tag_font = font(ANTON, 66)
    tag = "UNFILTERED!"
    tb = ImageDraw.Draw(canvas).textbbox((0, 0), tag, font=tag_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    box = Image.new("RGBA", (tw + 50, th + 34), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 0, box.width - 1, box.height - 1), radius=14, fill=(230, 20, 60))
    bd.text((box.width / 2, box.height / 2), tag, font=tag_font, fill=WHITE, anchor="mm")
    box = box.rotate(3, expand=True, resample=Image.BICUBIC)
    canvas.alpha_composite(box, (40, 500))

    # --- Gujarati tagline pill ---
    guj_font = font(GUJ, 38)
    guj = "ફિલ્મની વાતો • મસ્તી • ધમાલ"
    gb = ImageDraw.Draw(canvas).textbbox((0, 0), guj, font=guj_font)
    gw = gb[2] - gb[0]
    pill_y = 660
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((36, pill_y - 30, 36 + gw + 48, pill_y + 34), radius=32, fill=INK, outline=GOLD, width=3)
    d.text((36 + 24 + gw / 2, pill_y + 2), guj, font=guj_font, fill=WHITE, anchor="mm")

    # --- Corner badge on the photos ---
    badge_font = font(POPPINS, 26)
    d.rounded_rectangle((W - 230, 20, W - 20, 70), radius=25, fill=GOLD)
    d.ellipse((W - 210, 36, W - 192, 54), fill=(230, 20, 60))
    d.text((W - 112, 46), "EXCLUSIVE", font=badge_font, fill=INK, anchor="mm")

    canvas.convert("RGB").save(HERE / "thumbnail.png", optimize=True)
    canvas.convert("RGB").save(HERE / "thumbnail.jpg", quality=92)
    print("wrote thumbnail.png / thumbnail.jpg")


if __name__ == "__main__":
    main()
