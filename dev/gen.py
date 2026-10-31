# Writes src/full|half_horizontal|half_vertical|quadrant.liquid (the four views share their markup, so they are generated).
def graph(key, ticks='all', named=True, label='minutes'):
    full = key == 'full'
    return f'''<div class="qc-page qc-gr">
      {{%- assign variants = "o,x,p,m" | split: "," -%}}{{%- for v in variants -%}}
      {{%- if v == "o" -%}}{{%- assign tk = qc.tracks.{key}.o -%}}{{%- elsif v == "x" -%}}{{%- assign tk = qc.tracks.{key}.x -%}}{{%- elsif v == "p" -%}}{{%- assign tk = qc.tracks.{key}.p -%}}{{%- else -%}}{{%- assign tk = qc.tracks.{key}.m -%}}{{%- endif -%}}
      <svg class="qc-svg qc-{{{{ v }}}}" preserveAspectRatio="none" viewBox="0 0 {{{{ tk.w }}}} {{{{ tk.h }}}}">
        {{%- for t in tk.ticks -%}}<line class="qc-grid" x1="{{{{ tk.padl }}}}" x2="{{{{ tk.w }}}}" y1="{{{{ t.y }}}}" y2="{{{{ t.y }}}}"/>{{%- if tk.h > 100 -%}}<text class="qc-ax" x="{{{{ tk.padl | minus: 7 }}}}" y="{{{{ t.y | plus: 4 }}}}" text-anchor="end">{{{{ t.v }}}}</text>{{%- endif -%}}{{%- endfor -%}}
        {{%- for b in tk.bars -%}}<rect class="qc-col{{% if b.top == 1 %}} qc-col--top{{% endif %}}" x="{{{{ b.x }}}}" y="{{{{ b.y }}}}" width="{{{{ tk.bw }}}}" height="{{{{ b.h }}}}" rx="{{{{ tk.rx }}}}"/>{{%- if b.lab == 1 -%}}<text class="qc-bv" x="{{{{ b.cx }}}}" y="{{{{ b.y | minus: 5 }}}}" text-anchor="middle">{{{{ b.v }}}}</text>{{%- endif -%}}{{%- endfor -%}}
        <line class="qc-avg" x1="{{{{ tk.padl }}}}" x2="{{{{ tk.w }}}}" y1="{{{{ tk.avg }}}}" y2="{{{{ tk.avg }}}}"/>
        {{%- if tk.h > 100 -%}}<g transform="translate({{{{ tk.w | minus: 70 }}}},{{{{ tk.avg | minus: 12 }}}})"><rect class="qc-avgbox" width="64" height="24" rx="3"/><text class="qc-avgt" x="32" y="17.5" text-anchor="middle">avg {{{{ tk.avgv }}}}</text></g>{{%- endif -%}}
      </svg>
      {{%- endfor -%}}
    </div>'''
def rows(n, xonly_from, small=False, guests=5, tab=True, px_from=99):
    box = 'qc-qbox qc-qbox--s' if small else 'qc-qbox'
    tabs = '<div class="qc-tabs"><span class="qc-tab qc-t">Rides <span class="qc-s">{{ qc.open }}</span></span></div>\n      ' if tab else ''
    return f'''<div class="qc-right">
      {tabs}<div class="qc-page qc-list qc-grow">
      {{%- for r in qc.top limit: {n} -%}}
      <div class="qc-row qc-row--{{{{ r.heat }}}}{{% if r.rank == 1 %}} qc-row--sel{{% endif %}}{{% if forloop.index > {px_from} %}} qc-pxonly{{% elsif forloop.index > {xonly_from} %}} qc-xonly{{% endif %}}">
        <span class="qc-rn qc-clip qc-grow">{{{{ r.n }}}}</span>
        <span class="{box}">{{%- if r.q > 0 -%}}{{%- assign qn = r.q | at_most: {guests} -%}}{{%- assign qw = qn | times: 14 -%}}<svg class="qc-q" viewBox="0 0 {{{{ qw }}}} 17">{{%- for i in (1..qn) -%}}{{%- assign gi = i | times: 3 | plus: r.rank | modulo: 8 | plus: 1 -%}}<use href="#qc-g{{{{ gi }}}}" x="{{{{ i | minus: 1 | times: 14 }}}}"/>{{%- endfor -%}}</svg>{{%- else -%}}<span class="qc-s">walk-on</span>{{%- endif -%}}</span>
        <span class="qc-min">{{{{ r.w }}}}</span>
      </div>
      {{%- endfor -%}}
    </div></div>'''
TB = '<div class="qc-tb"><span class="qc-cb">X</span><span class="qc-t">{{ park_name }}</span><span class="qc-cap">Powered by Queue-Times.com</span></div>'
TBS = '<div class="qc-tb"><span class="qc-cb">X</span><span class="qc-t">{{ park_name }}</span></div>'
DAY = '{%- if qc.day -%}<div class="qc-day"><span class="qc-s">{{ qc.day.from }}</span><div class="qc-page qc-bar"><svg class="qc-barsvg" viewBox="0 0 100 10" preserveAspectRatio="none"><rect class="qc-barfill" width="{{ qc.day.pct }}" height="10"/><rect class="qc-barmark" x="{{ qc.day.pct | minus: 0.5 }}" width="1" height="10"/></svg></div><span class="qc-s">{{ qc.day.to }}</span><span class="qc-s qc-left">{{ qc.day.left }}</span></div>{%- endif -%}'
CROWD = '<fieldset class="qc-grp"><legend>Crowd</legend><div class="qc-gi">{{ ic_arch }}<div class="qc-page qc-gauge">{{ gauge }}</div><span class="qc-btn qc-t">{{ qc.level }}</span><span class="qc-grow"></span><span class="qc-s"><span class="qc-live"></span>{{ upd_l | date: "%H:%M" }} · {{ qc.open }}/{{ qc.total }} open · {% if qc.closes != "" %}until {{ qc.closes }} · {% endif %}avg {{ qc.avg }} min</span></div>' + DAY + '</fieldset>'
CROWD_S = '<div class="qc-row2"><div class="qc-crowd">{{ ic_arch }}<div class="qc-page qc-gauge">{{ gauge }}</div><span class="qc-btn qc-t">{{ qc.level }}</span></div><span class="qc-s">{{ qc.open }}/{{ qc.total }} open</span></div>'
NEWS = '<fieldset class="qc-grp qc-news"><legend>Guest says</legend><div class="qc-gi">{{ ic_face }}<span class="qc-t">{{ qc.thought }}</span></div></fieldset>'
GR = lambda key, t='all': f'<fieldset class="qc-grp qc-gfs"><legend>Queue lengths</legend>{graph(key, t)}</fieldset>'
OPEN = '{%- if qc.status == "open" -%}\n<div class="layout layout--col layout--stretch-x qc">\n  <div class="qc-w qc-grow">\n    ' + '{TB}' + '\n    <div class="qc-body">\n'
CLOSE = '\n    </div>\n  </div>\n</div>\n'
EMPTY = '''{%- else -%}
<div class="layout layout--col layout--stretch-x qc">{{ empty_screen }}</div>
{%- endif -%}
'''
def o(tb): return OPEN.replace('{TB}', tb)
files = {
 'full': o(TB) + f'      {CROWD}\n      {NEWS}\n      <div class="qc-split">\n    {GR("full")}\n    {rows(16, 12)}\n      </div>' + CLOSE + EMPTY,
 'half_horizontal': o(TBS) + f'      <div class="qc-split">\n    {graph("hh")}\n    {rows(8, 5, True, 5, False)}\n      </div>' + CLOSE + EMPTY,
 'half_vertical': o(TBS) + f'      {CROWD_S}\n      {graph("hv", "all", False)}\n    {rows(16, 7, True, 5, False, 14)}' + CLOSE + EMPTY,
 'quadrant': o(TBS) + f'      {graph("qd", "last", False)}\n    {rows(7, 3, True, 4, False, 4)}' + CLOSE + EMPTY,
}
for k, v in files.items(): open(f'src/{k}.liquid', 'w').write(v)
print('generated', ', '.join(files))
