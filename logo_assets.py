"""Derive the site's logo assets from the painted lockup.

`public/logo-source.webp` is the artwork as delivered: the Prompt Mala lockup
painted on a cream paper ground, 1536x1024. The site has its own paper, a shade
lighter, so pasting that rectangle into the masthead would show as a visible
box. Instead the ground is divided back out into an alpha channel — the lockup
is ink on paper, so each pixel's distance below the paper colour is how much ink
is there — and the result is trimmed to the artwork and written out at the sizes
the page asks for.

Composited over the paper it came from, the transparent version reproduces the
source exactly. Over the site's lighter paper it reads as the same painting on
that paper, which is the point. It is not meant for dark backgrounds: the pale
garland flowers are pale *ink*, and they go dark if you put them on ink.

Run from the repo root:

    python3 logo_assets.py
"""

import numpy as np
from PIL import Image

SOURCE = "public/logo-source.webp"

# The site's paper, --paper in the stylesheet. The social card and the icons are
# flattened onto it so they match the page they lead to.
PAPER = (244, 239, 228)

# Paper grain and the scan's vignette leave a little ink everywhere. Measured on
# the source, the artwork proper starts well above this and the noise sits well
# below it, so clearing it costs nothing and saves a tile of visible dirt.
GRAIN = 0.090

# Trim to where there is real ink, not to where the grain was.
INK = 0.12
PAD = 10

# The P, in pixels of the trimmed lockup: an icon at 32px has room for one
# letterform and no more. Taking it with the bud at its foot keeps a note of red
# in the tile, so it reads as this piece and not as a stray serif P.
ICON_GLYPH = (26, 88, 390, 420)
ICON_FILL = 0.82  # glyph box as a fraction of the tile

# The masthead draws the lockup about 230px wide at most. Shipping the full
# 1070 to do that is 240KB of detail nobody sees; this is still 2x on the
# widest layout and 3x on a phone.
MASTHEAD_W = 640


def lockup(path=SOURCE):
    """The lockup as RGBA, paper divided out and trimmed to the artwork."""
    src = Image.open(path).convert("RGB")
    a = np.asarray(src).astype(np.float32)

    # The paper is uniform within a few levels, so the border median is a good
    # enough estimate of it.
    border = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3),
                             a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    paper = np.median(border, axis=0)

    # Ink-on-paper: alpha is how far the most absorbed channel falls below the
    # paper, and the colour is what that ink must have been to land there.
    raw = np.clip(1.0 - (a / paper).min(axis=2), 0.0, 1.0)
    alpha = np.clip((raw - GRAIN) / (1.0 - GRAIN), 0.0, 1.0)
    safe = np.maximum(alpha, 1e-4)[..., None]
    colour = np.clip((a - paper * (1.0 - safe)) / safe, 0, 255)

    out = Image.fromarray(np.dstack([colour, alpha * 255.0]).astype(np.uint8), "RGBA")
    ys, xs = np.where(alpha > INK)
    return out.crop((max(int(xs.min()) - PAD, 0), max(int(ys.min()) - PAD, 0),
                     min(int(xs.max()) + 1 + PAD, out.width),
                     min(int(ys.max()) + 1 + PAD, out.height)))


def fit(img, box_w, box_h):
    """Scale to fit inside the box, keeping the aspect."""
    s = min(box_w / img.width, box_h / img.height)
    return img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))),
                      Image.LANCZOS)


def on_paper(img, size, fill):
    """Centre the image on a square of the site's paper."""
    w = h = size
    scaled = fit(img, int(w * fill), int(h * fill))
    tile = Image.new("RGB", (w, h), PAPER)
    tile.paste(scaled, ((w - scaled.width) // 2, (h - scaled.height) // 2), scaled)
    return tile


def main():
    mark = lockup()
    print(f"lockup trimmed to {mark.width}x{mark.height}")

    # The masthead image. The alpha channel, not the colour, is what costs here:
    # storing it lossily takes the file from 94KB to 54KB with no edge artefact
    # visible at the size the masthead draws it.
    fit(mark, MASTHEAD_W, mark.height).save(
        "public/logo.webp", quality=82, alpha_quality=70, method=6)

    # The icons. One letterform, flattened onto paper so the tile is opaque.
    glyph = mark.crop(ICON_GLYPH)
    for size in (32, 180, 512):
        on_paper(glyph, size, ICON_FILL).save(f"public/icon-{size}.png", optimize=True)

    # The social card, at the 1.91:1 the scrapers crop to.
    card = Image.new("RGB", (1200, 630), PAPER)
    art = fit(mark, 820, 470)
    card.paste(art, ((1200 - art.width) // 2, (630 - art.height) // 2), art)
    card.save("public/og.png", optimize=True)

    print("wrote public/logo.webp, public/icon-{32,180,512}.png, public/og.png")


if __name__ == "__main__":
    main()
