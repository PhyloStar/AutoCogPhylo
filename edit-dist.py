from lingpy import *
from glob import glob
from collections import defaultdict
from lingpy.evaluate.acd import bcubes

files = sorted(glob('data/data-*.tsv'))
for f in files:
    print('[i] Analyzing...', f)
    wl = LexStat(f)
    wl.cluster(method='edit-dist', threshold=0.75, ref='editid')
    wl.add_entries('inferred_class', 'concept,editid', lambda x, y: 
            x[y[0]]+':'+str(x[y[1]]))
    wlx = Wordlist(f)
    cols = wlx.columns + ['inferred_class', 'editid']
    
    wl.output('tsv', filename='computed/'+f.split('/')[1].replace('data-',
        'edit-')[:-4], ignore='all', prettify=False, subset=True, cols=cols)
    wl.output('paps.nex', ref='editid', missing='?',
            filename='nexus/'+f.split('/')[1].replace('data', 'edit')[:-4])
    p, r, f = bcubes(wl, 'cogid', 'editid', pprint=False)
    print('... {0:.2f} {1:.2f} {2:.2f}'.format(p, r, f))

