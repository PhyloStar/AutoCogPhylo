from lingpy import *
from lingpy.convert.cldf import to_cldf
from pyconcepticon.api import Concepticon

con = Concepticon()

data = [
    "data-aa-58-200.tsv",
    "data-an-45-210.tsv",
    "data-ie-42-208.tsv",
    "data-pn-67-183.tsv",
    "data-st-64-110.tsv"
    ]

conceptlists = [
        'Sidwell-2015-200',
        'Blust-2008-210',
        'Dunn-2012-207',
        'Bowern-2011-204',
        'Starostin-1991-110'
        ]


name2gcode = {n: g for n, g in csv2list('langs_glottocode_list.txt',
    strip_lines=False)[1:]}

for i, f in enumerate(data):
    wl = Wordlist('data/'+f)
    if not 'glottocode' in wl.header:
        wl.add_entries('glottocode', 'doculect', lambda x: name2gcode.get(x, ''))
    if i != 3:
        clist = {c[1].english or c[1].gloss : c[1].concepticon_id for c in
                con.conceptlists[conceptlists[i]].concepts.items()}
        for idx, concept, cid in wl.iter_rows('concept', 'concepticon_id'):
            wl[idx, 'concepticon_id'] = clist.get(concept, '') or clist.get(concept.lower(), '')
    else:
        g2c = {c.gloss: c.id for c in con.conceptsets.values()}
        for idx, cid in wl.iter_rows('concept'):
            wl[idx, 'concepticon_id'] = g2c.get(cid, '')
    to_cldf(wl, path='cldf/'+f.split('-')[1]+'-cldf')
