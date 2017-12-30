from lingpy import *
from glob import glob
from collections import defaultdict
from lingpy.evaluate.acd import bcubes

def turchin(wordlist):
    CC = {}
    for concept in wl.rows:
        words = wl.get_list(row=concept, flat=True)
        cogs = defaultdict(list)
        for w in words:
            dolgo = wordlist[w, 'dolgo'].split()
            if 'V' in dolgo and len(set(dolgo)) == 1:
                # the turchin rule: every word is treated as two sounds,
                # initial vowel is laryngeal
                cls = 'HH'
            elif dolgo[0] == 'V' and dolgo[1] != 'V':
                cls = 'H'+dolgo[1]
            elif len([c for c in dolgo if c != 'V']) == 1:
                cls = dolgo[0] + 'H'
            else:
                cls = ''.join([c for c in dolgo if c != 'V'][:2])
            cogs[cls] += [w]
        for i, (cog, words) in enumerate(cogs.items()):
            for word in words:
                CC[word] = concept + ':' + cog
    wordlist.add_entries('inferred_class', CC, lambda x: x)
    wordlist.renumber('inferred_class', 'turchinid')


files = sorted(glob('data/data-*.tsv'))
for f in files:
    print('[i] Analyzing...', f)
    wl = Wordlist(f)
    turchin(wl)
    wl.output('tsv', filename='computed/'+f.split('/')[1].replace('data-',
        'turchin-')[:-4], ignore='all', prettify=False)
    wl.output('paps.nex', ref='turchinid', missing='?',
            filename='nexus/'+f.split('/')[1].replace('data', 'turchin')[:-4])
    p, r, f = bcubes(wl, 'cogid', 'turchinid', pprint=False)
    print('... {0:.2f} {1:.2f} {2:.2f}'.format(p, r, f))

