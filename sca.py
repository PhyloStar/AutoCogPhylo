from lingpy import *
from glob import glob
from collections import defaultdict
from lingpy.evaluate.acd import bcubes

files = sorted(glob('data/data-*.tsv'))
for f in files:
    print('[i] Analyzing...', f)
    wl = LexStat(f)
    wl.cluster(method='sca', threshold=0.45, ref='scaid')
    wl.add_entries('inferred_class', 'concept,scaid', lambda x, y: 
            x[y[0]]+':'+str(x[y[1]]))
    wlx = Wordlist(f)
    cols = wlx.columns + ['inferred_class', 'scaid']
    
    wl.output('tsv', filename='computed/'+f.split('/')[1].replace('data-',
        'sca-')[:-4], ignore='all', prettify=False, subset=True, cols=cols)
    wl.output('paps.nex', ref='scaid', missing='?',
            filename='nexus/'+f.split('/')[1].replace('data', 'sca')[:-4])
    p, r, f = bcubes(wl, 'cogid', 'scaid', pprint=False)
    print('... {0:.2f} {1:.2f} {2:.2f}'.format(p, r, f))

