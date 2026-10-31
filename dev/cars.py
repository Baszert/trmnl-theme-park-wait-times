# Pixel-art coaster car, pre-rendered for every slope (like the sprite sheets in the real game), in the same palette as the guests.
# The car is drawn at 10x, rotated about the point on the rail centre line, then reduced to the pixel grid: black ink where the lines cover
# enough of a pixel, a flat gray level where a fill does, nothing elsewhere. Output: ASCII rows with K black, D, G, L grays, W white.
import math
from PIL import Image, ImageDraw
S = 10                 # supersampling
N = 64                 # sprite canvas in pixels
AX, AY = 32.5, 50      # anchor (on the rail centre line) in the canvas
ANGLES = [-72 + 12 * i for i in range(13)]   # -72 .. 72 degrees
LEVEL = {'W': 255, 'L': 200, 'G': 140, 'D': 70}

def render(angle):
    ink = Image.new('L', (N * S, N * S), 0); fill = Image.new('L', (N * S, N * S), 0); shape = Image.new('L', (N * S, N * S), 0)
    di, df, ds = ImageDraw.Draw(ink), ImageDraw.Draw(fill), ImageDraw.Draw(shape)
    a = math.radians(angle); ca, sa = math.cos(a), math.sin(a)
    def P(x, y):   # local car coords (x forward, y up negative, origin = wheel contact below the anchor) -> canvas
        y -= 2.5
        return ((AX + x * ca - y * sa) * S, (AY + x * sa + y * ca) * S)
    def poly(pts, level=None, ink_w=0, close=True):
        q = [P(*p) for p in pts]
        if level is not None: df.polygon(q, fill=LEVEL[level]); ds.polygon(q, fill=255)
        if ink_w:
            di.line(q + ([q[0]] if close else []), fill=255, width=int(ink_w * S), joint='curve')
    def circle(cx, cy, r, level=None, ink_w=0):
        x, y = P(cx, cy); rr = r * S
        if level is not None: df.ellipse([x - rr, y - rr, x + rr, y + rr], fill=LEVEL[level]); ds.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
        if ink_w: di.ellipse([x - rr, y - rr, x + rr, y + rr], outline=255, width=int(ink_w * S))
    def dot(cx, cy, r):
        x, y = P(cx, cy); rr = r * S; di.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255); ds.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
    def line(p, q, w):
        a_, b_ = P(*p), P(*q); di.line([a_, b_], fill=255, width=int(w * S)); ds.line([a_, b_], fill=255, width=int(w * S))
    def rider(cx, shirt, hair):
        # arms up with hands, a torso in a shirt, a head with a cap of hair, eyes and an open mouth
        line((cx - 3, -21), (cx - 6, -30), 1.0); line((cx + 3, -21), (cx + 6, -30), 1.0)
        circle(cx - 6, -31, 1.6, 'W', 1.0); circle(cx + 6, -31, 1.6, 'W', 1.0)
        poly([(cx - 4, -17), (cx - 4, -21), (cx - 2, -23), (cx + 2, -23), (cx + 4, -21), (cx + 4, -17)], shirt, 1.0)
        circle(cx, -27, 3.6, 'W', 1.0)
        q = [P(cx + 3.6 * math.cos(t), -27 + 3.6 * math.sin(t)) for t in [math.pi + 0.45 + i * (math.pi - 0.9) / 10 for i in range(11)]]
        if hair == 'K': di.polygon(q, fill=255); ds.polygon(q, fill=255)
        else: df.polygon(q, fill=LEVEL[hair]); ds.polygon(q, fill=255); di.line(q, fill=255, width=S)
        dot(cx - 1.4, -26.4, 0.55); dot(cx + 1.4, -26.4, 0.55)
        x, y = P(cx, -24.6); di.ellipse([x - 0.8 * S, y - 0.9 * S, x + 0.8 * S, y + 0.9 * S], fill=255)
    rider(-7, 'G', 'D'); rider(6, 'L', 'K')
    poly([(-17, -8), (-17, -14), (-14, -17), (11, -17), (17, -13), (22, -11), (22, -8)], 'W', 1.0)
    poly([(-17, -13), (21, -13), (21, -10), (-17, -10)], 'D')                  # stripe
    di.line([P(-17, -13), P(21, -13)], fill=255, width=S); di.line([P(-17, -10), P(21, -10)], fill=255, width=S)
    poly([(13, -16), (20, -12), (21, -10), (13, -10)], 'L')                    # nose highlight
    line((-12, -18), (9, -18), 1.2)                                            # lap bar
    poly([(-15, -8), (-15, -5), (15, -5), (15, -8)], 'D', 1.0)                 # chassis
    dot(21, -12, 0.9)                                                          # headlight
    line((-17, -12), (-21, -12), 1.0); line((-17, -15), (-23, -15), 1.0)       # speed lines
    for wx in (-9, 9):
        circle(wx, -3.5, 3.6, 'W', 1.0); dot(wx, -3.5, 0.8)
    # reduce to the pixel grid
    ink_s = ink.resize((N, N), Image.BOX); shape_s = shape.resize((N, N), Image.BOX); fill_s = fill.resize((N, N), Image.BOX)
    rows = []
    for y in range(N):
        row = ''
        for x in range(N):
            i, sh, f = ink_s.getpixel((x, y)), shape_s.getpixel((x, y)), fill_s.getpixel((x, y))
            if i >= 118: row += 'K'
            elif sh >= 130:
                lv = f * 255 / max(sh, 1); row += min(LEVEL, key=lambda k: abs(LEVEL[k] - lv))
            else: row += '.'
        rows.append(row)
    return rows

def sprites():
    return {f'car{k}': '\n'.join(render(a)) for k, a in enumerate(ANGLES)}

if __name__ == '__main__':
    out = Image.new('L', (N * 13 * 4, N * 4), 200)
    pal = {'K': 0, 'W': 255, 'L': 215, 'G': 150, 'D': 80, '.': 200}
    for k, a in enumerate(ANGLES):
        for y, r in enumerate(render(a)):
            for x, ch in enumerate(r):
                out.paste(pal[ch], (k * N * 4 + x * 4, y * 4, k * N * 4 + x * 4 + 4, y * 4 + 4))
    out.save('/private/tmp/claude-501/-Users-bas/cf136e84-eae5-478f-a99e-1b83f190ded3/scratchpad/cars.png'); print('ok')
