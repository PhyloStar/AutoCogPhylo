from lingpy import *
from glob import glob
from collections import defaultdict
from lingpy.evaluate.acd import bcubes

files = sorted(glob('data/data-*.tsv'))
for f in files:
    print('[i] Analyzing...', f)
    try:
        wl = LexStat(f.replace('data', 'bins'))
    except:
        print('re-calculating')
        wl = LexStat(f)
        wl.get_scorer(runs=10000)
        wl.output('tsv', filename=f.replace('data', 'bins')[:-4], ignore='')

    wl.cluster(method='lexstat', cluster_method='infomap', threshold=0.55,
            ref='infomapid')
    wl.cluster(method='lexstat', cluster_method='upgma', threshold=0.6, 
            ref='lexstatid')
    wl.add_entries('inferred_class', 'concept,infomapid', lambda x, y: 
            x[y[0]]+':'+str(x[y[1]]))
    wlx = Wordlist(f)
    cols = wlx.columns + ['inferred_class', 'infomapid']
    
    wl.output('tsv', filename='computed/'+f.split('/')[1].replace('data-',
        'infomap-')[:-4], ignore='all', prettify=False, subset=True, cols=cols)
    wl.output('paps.nex', ref='infomapid', missing='?',
            filename='nexus/'+f.split('/')[1].replace('data', 'infomap')[:-4])
    p, r, fc = bcubes(wl, 'cogid', 'lexstatid', pprint=False)
    print('*', f.split('/')[1].replace('data-', ''), '| {0:.2f} | {1:.2f} | {2:.2f}'.format(p, r, fc))
    p, r, fc = bcubes(wl, 'cogid', 'infomapid', pprint=False)
    print(f.split('/')[1].replace('data-', ''), '| {0:.2f} | {1:.2f} | {2:.2f}'.format(p, r, fc))


