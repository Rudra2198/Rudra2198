import io, re, cairosvg
from PIL import Image

SRC = open("assets/banner.svg").read()
SRC = re.sub(r"@font-face \{.*?\}", "", SRC, flags=re.S)
SRC = SRC.replace('"Orb", "Arial Narrow"', '"Orbitron", "Arial Narrow"')
SRC = SRC.replace('"Raj", "Arial Narrow"', '"Rajdhani", "Arial Narrow"')

LOOP, N, W = 3.4, 34, 760


def frame(t):
    s = SRC
    # tear A: 3.4s cycle, band 190 wide, content shifted +9/-3
    ax = -190 + (t / 3.4) * 1390
    s = s.replace('<rect x="-190" y="0" width="190" height="340">',
                  f'<rect x="{ax:.1f}" y="0" width="190" height="340">')
    # tear B: 2.3s cycle, band 70 wide, content shifted -7/+2
    bx = -70 + ((t % 2.3) / 2.3) * 1270
    s = s.replace('<rect x="-70" y="0" width="70" height="340">',
                  f'<rect x="{bx:.1f}" y="0" width="70" height="340">')
    # leading edges ride the front of each band
    s = s.replace('<rect x="-4" y="0" width="2" height="340" fill="#00f0ff" opacity="0.55">',
                  f'<rect x="{ax + 190:.1f}" y="0" width="2" height="340" fill="#00f0ff" opacity="0.55">')
    s = s.replace('<rect x="-4" y="0" width="2" height="340" fill="#ff003c" opacity="0.4">',
                  f'<rect x="{bx + 70:.1f}" y="0" width="2" height="340" fill="#ff003c" opacity="0.4">')
    # cursor blink, 0.9s cycle
    if (t % 0.9) >= 0.45:
        s = s.replace(f'<rect x="213.0" y="135" width="12" height="25" fill="#fcee0a">',
                      f'<rect x="213.0" y="135" width="12" height="25" fill="#fcee0a" opacity="0">')
    # RAM units 7 and 8 cycling, 2.6s
    for i, off in ((6, 0.0), (7, 0.45)):
        if 0.5 <= ((t - off) % 2.6) <= 1.5:
            x = 916 + i * 20
            old = f'<path d="M {x + 4},22 L {x + 15},22 L {x + 15},48 L {x},48 L {x},26 Z" fill="#00f0ff">'
            s = s.replace(old, old[:-1] + ' opacity="0.18">')
    s = re.sub(r"<animate[^>]*/>", "", s)
    s = re.sub(r"<animate[^>]*>.*?</animate>", "", s, flags=re.S)
    png = cairosvg.svg2png(bytestring=s.encode(), output_width=W)
    return Image.open(io.BytesIO(png)).convert("RGB")


frames = [frame(i / N * LOOP) for i in range(N)]
frames[0].save("preview.gif", save_all=True, append_images=frames[1:],
               duration=int(LOOP * 1000 / N), loop=0, optimize=True)
print(f"preview.gif: {N} frames, {LOOP}s loop")
