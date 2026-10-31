# Pixel sprites for Queue Coaster: one hidden <svg> of <g> sprites that every view <use>s (1 sprite pixel = 2 device pixels).
# K black, D dark gray, G gray, L light gray, W white, . transparent. Grays are 1-device-pixel dither patterns; 4-bit screens get real grays via CSS.
import re, math
ART = {
# thought-bubble guest (bigger, 9 x 13)
'hero': """
...KKK...
..KKKKK..
..KWWWK..
..KWKWK..
..KWWWK..
...KKK...
..KDDDK..
.KKDDDKK.
KWKDDDKWK
.K.DDD.K.
...KGK...
...K.K...
..KK.KK..""",
# scenery, light gray
'pine': """
...G...
..GGG..
..GGG..
.GGGGG.
.GGGGG.
GGGGGGG
...G...
...G...""",
'tent': """
.......GG.......
.......G.G......
......GGGG......
.....GGGGGG.....
....GGGGGGGG....
...GGGGGGGGGG...
..GGGGGGGGGGGG..
.GGGGGGGGGGGGGG.
GGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGG""",
'tower': """
.GGG.
.GGG.
..G..
..G..
.GGG.
..G..
..G..
.GGG.
..G..
..G..
.GGG.
..G..
..G..
.GGG.
..G..
.GGG.
GGGGG
.GGG.
.G.G.
.G.G.""",
# park entrance (header) 18 x 14
'arch': """
K................K
KK..............KK
KDK....KKKK....KDK
KDK...KGGGGK...KDK
KDKKKKKGWWGKKKKDKK
KDDDDDKGGGGKDDDDDK
KDGGGDKKKKKKDGGGDK
KDGGGDK....KDGGGDK
KDGGGDK....KDGGGDK
KDDDDDK....KDDDDDK
KKKKKKK....KKKKKKK""",
# closed gate (big, 24 x 16)
'gate': """
.KK..................KK.
KWWK................KWWK
.KK..................KK.
.KK..K.K.K.K.K.K.K...KK.
.KD..K.K.K.K.K.K.K...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..KKKKKKKKKKKKK...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..KKKKKKKKKKKKK...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..K.K.K.K.K.K.K...DK.
.KD..K.K.K.K.K.K.K...DK.
KKKKKKKKKKKKKKKKKKKKKKKK""",
# padlock (6 x 8)
'lock': """
.KKKK.
K....K
K....K
KKKKKK
KGGGGK
KGKKGK
KGGGGK
KKKKKK""",
}

# Detailed guests (13 x 17, drawn at 1 device pixel per sprite pixel): hair, face with eyes and mouth, a striped shirt, arms and hands, trousers, shoes, and sometimes a balloon.
def guest(kind, hair, shirt, pants, stripe=None, balloon=False):
    h, s_, p, t = hair, shirt, pants, stripe or shirt
    head = ['..KKKKK..', f'.K{h*5}K.', f'.K{h*5}K.', '.KWWWWWK.', '.KWKWKWK.', '.KWWKWWK.', '..KWWWK..']
    if kind == 'cap':
        head = ['..KKKKK..', f'.K{t*5}K.', f'KKK{t*3}KKK', '.KWWWWWK.', '.KWKWKWK.', '.KWWKWWK.', '..KWWWK..']
    if kind == 'long':
        head = ['..KKKKK..', f'.K{h*5}K.', f'K{h*7}K', f'K{h}KWWWK{h}K', f'K{h}KKWKK{h}K', f'K{h}KWKWK{h}K', f'K{h}{h}KWK{h}{h}K']
    arms = [f'.K{s_*5}K.', f'K{t*7}K', f'K{s_}K{s_*3}K{s_}K', 'KWK' + s_ * 3 + 'KWK', '.KK' + s_ * 3 + 'KK.']
    legs = [f'..K{p*3}K..', f'..K{p}K{p}K..', f'..K{p}K{p}K..', f'..K{p}K{p}K..', '.KKK.KKK.']
    if kind == 'yay':
        head[0] = 'W.KKKKK.W'; head[1] = f'KWK{h*3}KWK'[:3] + h * 3 + 'KWK'; head[2] = f'.KK{h*3}KK.'[:9] if False else f'.K{h*5}K.'
        head[1] = 'KWK' + h * 3 + 'KWK'; head[2] = '.K' + h * 5 + 'K.'
        arms = [f'.K{s_*5}K.', f'.K{t*5}K.', f'..K{s_*5}K..'[:9], f'..K{s_*5}K..'[:9], '..K' + s_ * 3 + 'K..']
        arms = ['.K' + s_ * 5 + 'K.', '.K' + t * 5 + 'K.', '..K' + s_ * 3 + 'K..', '..K' + s_ * 3 + 'K..', '..KKKKK..']
    if kind == 'dress':
        arms = ['.K' + s_ * 5 + 'K.', 'K' + t * 7 + 'K', 'KWK' + s_ * 3 + 'KWK', '.K' + s_ * 5 + 'K.', 'K' + s_ * 7 + 'K']
        legs = ['K' + s_ * 7 + 'K', '.KWK.KWK.', '.KKK.KKK.']
    if kind == 'kid':
        arms = ['.K' + s_ * 5 + 'K.', 'KWK' + s_ * 3 + 'KWK']
        legs = ['..K' + p * 3 + 'K..', '..KpK' .replace('p', p) + p + 'K..', '.KKK.KKK.']
    rows = [r[:9].ljust(9, '.') for r in head + arms + legs]
    H = 17; g = [['.'] * 13 for _ in range(H)]; off = H - len(rows)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r): g[off + y][x] = ch
    if balloon:
        for y, r in enumerate(['.KK.', 'KLLK', 'KLLK', '.KK.', '..K.']):
            for x, ch in enumerate(r):
                if ch != '.': g[y][9 + x] = ch
        hand = next(y for y, r in enumerate(g) if r[7] == 'W' and y > off + 7)
        for y in range(5, hand): g[y][10] = 'K'
        g[hand][9] = 'K'; g[hand][10] = 'K'
    return '\n'.join(''.join(r) for r in g)
ART['g1'] = guest('man', 'D', 'G', 'D', 'L')
ART['g2'] = guest('cap', 'K', 'G', 'D', 'L')
ART['g3'] = guest('long', 'L', 'D', 'G')
ART['g4'] = guest('dress', 'K', 'G', 'D', 'L')
ART['g5'] = guest('kid', 'D', 'L', 'D', balloon=True)
ART['g6'] = guest('yay', 'K', 'G', 'D', 'L')
ART['g7'] = guest('man', 'L', 'K', 'G', 'L')
ART['g8'] = guest('cap', 'D', 'L', 'D', 'G')
def wheel(r=14):
    n = 2 * r + 3; g = [['.'] * n for _ in range(n)]; c = r + 1
    for a in range(0, 360, 3):
        x = round(c + r * math.cos(math.radians(a))); y = round(c + r * math.sin(math.radians(a))); g[y][x] = 'G'
    for a in range(0, 360, 45):
        for t in range(1, r):
            x = round(c + t * math.cos(math.radians(a))); y = round(c + t * math.sin(math.radians(a)))
            if g[y][x] == '.': g[y][x] = 'G' if t % 2 else 'L'
    for a in range(0, 360, 45):
        x = round(c + r * math.cos(math.radians(a))); y = round(c + r * math.sin(math.radians(a)))
        for dy in (0, 1):
            for dx in (0, 1): g[min(y + dy, n - 1)][min(x + dx, n - 1)] = 'K'
    g[c][c] = 'K'
    legs = []
    for t in range(0, 10):
        legs.append(['.'] * n)
        l = c - 1 - t // 2; rr = c + 1 + t // 2
        if 0 <= l < n: legs[-1][l] = 'L'
        if 0 <= rr < n: legs[-1][rr] = 'L'
    return '\n'.join(''.join(row) for row in g + legs)
ART['wheel'] = wheel()
FILL = {'K': ('', '#000'), 'W': ('', '#fff'), 'D': ('d', 'var(--qc-d,url(#qcp-d))'), 'G': ('g', 'var(--qc-g,url(#qcp-g))'), 'L': ('l', 'var(--qc-l,url(#qcp-l))')}
# Dither cells are half a sprite pixel: one device pixel when the sprite is drawn at 2x.
DEFS = ('<defs>'
        '<pattern id="qcg-d" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#000"/><rect x="1" y="1" width="1" height="1" fill="#fff"/></pattern>'
        '<pattern id="qcg-g" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect width="1" height="1" fill="#000"/><rect x="1" y="1" width="1" height="1" fill="#000"/></pattern>'
        '<pattern id="qcg-l" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff"/><rect width="1" height="1" fill="#000"/></pattern>'
        '<pattern id="qcp-w" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#000"/><rect width="1" height="1" fill="#fff"/></pattern>'
        '<pattern id="qcp-d" width="1" height="1" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#000"/><rect x="0.5" y="0.5" width="0.5" height="0.5" fill="#fff"/></pattern>'
        '<pattern id="qcp-g" width="1" height="1" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#fff"/><rect width="0.5" height="0.5" fill="#000"/><rect x="0.5" y="0.5" width="0.5" height="0.5" fill="#000"/></pattern>'
        '<pattern id="qcp-l" width="1" height="1" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#fff"/><rect width="0.5" height="0.5" fill="#000"/></pattern>')
def group(name, art):
    # classes instead of inline styles: k black, w white, d g l the guest grays (1 px dither), pd pg pl the grays of the 2x sprites
    guest = bool(re.fullmatch(r'g\d', name))
    cls = {'K': 'qk', 'W': 'qw', 'D': 'qd' if guest else 'qpd', 'G': 'qg' if guest else 'qpg', 'L': 'ql' if guest else 'qpl'}
    rows = art.strip('\n').split('\n'); out = []
    for y, r in enumerate(rows):
        for ch, c in cls.items():
            for m in re.finditer(ch + '+', r):
                out.append(f'<rect class="{c}" x="{m.start()}" y="{y}" width="{m.end() - m.start()}" height="1"/>')
    return f'<g id="qc-{name}">{"".join(out)}</g>', max(len(r) for r in rows), len(rows)
for k in ['hero','pine','tent','tower','lock','wheel']: ART.pop(k, None)
body, sizes = '', {}
for k, v in ART.items():
    g, w, h = group(k, v); body += g; sizes[k] = (w, h)
svg = f'<svg class="qc-defs" width="0" height="0" shape-rendering="crispEdges" aria-hidden="true">{DEFS}{body}</defs></svg>'
svg = svg.replace('</defs></svg>', '</defs></svg>')
block = '{%- comment -%} Sprites (generated by dev/sprites.py, do not edit by hand). {%- endcomment -%}\n' + svg + '\n{%- comment -%} /Sprites {%- endcomment -%}\n'
p = 'src/shared.liquid'; s = open(p).read()
s = re.sub(r'\{%- comment -%\} Sprites \(generated.*?/Sprites \{%- endcomment -%\}\n', lambda m: block, s, flags=re.S)
open(p, 'w').write(s)
print('sprites:', ', '.join(f'{k} {w}x{h}' for k, (w, h) in sizes.items()))
