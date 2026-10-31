# Theme Park Wait Times icon in the house template (512x512): shadow plate, lighter face, 20 px black strokes.
# A "45" sign over a queue of guests, drawn from the same pixel sprites as the screen.
import sys, io, contextlib
sys.path.insert(0, 'dev')
with contextlib.redirect_stdout(io.StringIO()):
    import sprites as sp
COL = {'K': '#000', 'W': '#fff', 'D': '#4a4a4a', 'G': '#8c8c8c', 'L': '#cfcfcf'}
def pix(art, ox, oy, u):
    out = []
    for y, r in enumerate(art.strip('\n').split('\n')):
        for x, ch in enumerate(r):
            if ch in COL: out.append(f'<rect x="{ox + x * u}" y="{oy + y * u}" width="{u}" height="{u}" fill="{COL[ch]}"/>')
    return ''.join(out)
DIG = {'4': ['X.X', 'X.X', 'XXX', '..X', '..X'], '5': ['XXX', 'X..', 'XXX', '..X', 'XXX']}
def digits(text, ox, oy, u):
    out = ''
    for i, d in enumerate(text):
        for y, r in enumerate(DIG[d]):
            for x, ch in enumerate(r):
                if ch == 'X': out += f'<rect x="{ox + (i * 4 + x) * u}" y="{oy + y * u}" width="{u}" height="{u}" fill="#fff"/>'
    return out
U = 10
GY = 218
guests = ''.join(pix(sp.ART[k], 30 + i * 14 * U + (0 if i else 6), GY, U) for i, k in enumerate(['g1', 'g4', 'g5']))
CLOUD = ['..XXX..', '.XXXXX.', 'XXXXXXX']
cloud = lambda ox, oy, u: ''.join(f'<rect x="{ox + x * u}" y="{oy + y * u}" width="{u}" height="{u}" fill="#fff"/>' for y, r in enumerate(CLOUD) for x, ch in enumerate(r) if ch == 'X')
sign = cloud(60, 84, 12) + cloud(300, 140, 10)
open('icon.svg', 'w').write(f'''<svg width="512" height="512" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<clipPath id="face"><rect x="10" y="10" width="453" height="454" rx="50"/></clipPath>
</defs>
<rect x="10" y="10" width="492" height="492" rx="90" fill="#1D5A7A"/>
<rect x="10" y="10" width="492" height="492" rx="90" stroke="black" stroke-width="20"/>
<rect x="10" y="10" width="453" height="454" rx="50" fill="#7CCBEF"/>
<g clip-path="url(#face)" shape-rendering="crispEdges">
<rect x="0" y="{GY + 17 * U - 4}" width="480" height="200" fill="#4FA63E"/>
<rect x="0" y="{GY + 17 * U - 14}" width="480" height="16" fill="black"/>
{sign}
{guests}
</g>
<rect x="10" y="10" width="453" height="454" rx="50" stroke="black" stroke-width="20"/>
</svg>
''')
