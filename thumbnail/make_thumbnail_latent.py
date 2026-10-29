"""Cast-cluster thumbnail ("India's Got Latent" style) for Kamal Chhe Tu Kaku.

Cut-out cast members overlap in a cluster on the magenta stage, the bottom
fades to black, and the film logo sits big and centred along the bottom.

Cut-outs live in cutouts/ (made with cutouts/cut.py from the original photos).
Usage: python3 make_thumbnail_latent.py  ->  thumbnail-latent.png / .jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from make_thumbnail import ANTON, GOLD, GUJ, INK, RED, WHITE, font, keyed_logo, tag, text_block

HERE = Path(__file__).parent
W, H = 1280, 720

# Each cast member: source cut-out, crop box (source px), head centre-x and
# head top (source px), scale, and where that head point lands on the canvas.
# Listed back to front.
CAST = [
    # red top, laughing (back row, left)
    dict(src="group.png", crop=(0, 340, 380, 941), head=(240, 370), scale=1.15, at=(400, 92)),
    # orange tee, looking toward the centre (front, right)
    dict(src="cast-1.png", crop=(1000, 100, 2000, 1333), head=(1475, 140), scale=0.50, at=(1050, 118)),
    # blue dupatta, laughing (front, left)
    dict(src="cast-2.png", crop=(0, 380, 1000, 1333), head=(515, 420), scale=0.68, at=(215, 196)),
    # light-blue shirt, laughing (centre, biggest)
    dict(src="cast-2.png", crop=(900, 360, 2000, 1333), head=(1150, 390), scale=0.82, at=(660, 58)),
]


def stage_background():
    """Magenta stage with gold rings, taken from the clean top of the group photo."""
    src = Image.open(HERE / "cast-group.webp").convert("RGB")
    top = src.crop((0, 0, src.width, 365)).resize((W, 560), Image.LANCZOS)
    bg = Image.new("RGB", (W, H), (20, 0, 24))
    bg.paste(top, (0, 0))
    # Blend the seam at y=560 into the dark floor
    fade = Image.linear_gradient("L").resize((W, 160)).point(lambda v: 255 - v)
    bg.paste(top.crop((0, 400, W, 560)), (0, 400), fade)
    return bg.convert("RGBA")


def place(canvas, person):
    cut = Image.open(HERE / "cutouts" / person["src"]).convert("RGBA").crop(person["crop"])
    s = person["scale"]
    cut = cut.resize((int(cut.width * s), int(cut.height * s)), Image.LANCZOS)
    cut = ImageEnhance.Contrast(cut).enhance(1.06)
    hx = (person["head"][0] - person["crop"][0]) * s
    hy = (person["head"][1] - person["crop"][1]) * s
    x, y = int(person["at"][0] - hx), int(person["at"][1] - hy)

    # Soft shadow so each person separates from whoever is behind them
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((10, 0, 15, 110), (x, y + 6), cut.getchannel("A"))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(cut, (x, y), cut)
    canvas.alpha_composite(layer)


def bottom_fade(canvas, start=360):
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    for y in range(start, H):
        t = (y - start) / (H - start)
        d.line([(0, y), (W, y)], fill=int(250 * min(1, t ** 1.3 * 1.25)))
    shade = Image.new("RGBA", (W, H), (8, 0, 10, 255))
    shade.putalpha(g)
    canvas.alpha_composite(shade)


def main():
    canvas = stage_background()
    for person in CAST:
        place(canvas, person)
    bottom_fade(canvas)

    # --- Kicker line above the logo (like "INDIA'S GOT") ---
    kick = font(ANTON, 50)
    left, right = "STAR CAST ", "UNFILTERED!"
    d = ImageDraw.Draw(canvas)
    lw = d.textlength(left, font=kick)
    rw = d.textlength(right, font=kick)
    x0 = (W - lw - rw) / 2
    ky = 412
    text_block(canvas, (x0, ky), left, kick, WHITE, stroke=4)
    text_block(canvas, (x0 + lw, ky), right, kick, GOLD, stroke=4)

    # --- The film logo, big and centred along the bottom ---
    logo = keyed_logo()
    logo_h = 230
    logo = logo.resize((int(logo.width * logo_h / logo.height), logo_h), Image.LANCZOS)
    lx, ly = (W - logo.width) // 2, 478
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 200), (lx + 6, ly + 8), logo.getchannel("A"))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    canvas.alpha_composite(logo, (lx, ly))

    # --- Gujarati tagline, bottom corners stay clear for the cast ---
    gf = font(GUJ, 30)
    guj = "ફિલ્મની વાતો • મસ્તી • ધમાલ"
    text_block(canvas, (W / 2, H - 8), guj, gf, WHITE, stroke=3, anchor="ms")

    canvas.convert("RGB").save(HERE / "thumbnail-latent.png", optimize=True)
    canvas.convert("RGB").save(HERE / "thumbnail-latent.jpg", quality=92)
    print("wrote thumbnail-latent.png / thumbnail-latent.jpg")


if __name__ == "__main__":
    main()
