from lingpy import *
from glob import glob
from lingpy.evaluate.acd import *

for ds in glob('data/data-*.tsv'):
    wl = Wordlist(ds)
    wl.add_entries('nid', {x: x for x in wl}, lambda x: x)
    p1, r1, f1 = bcubes(wl, 'cogid', 'concept', pprint=False)
    p2, r2, f2 = bcubes(wl, 'cogid', 'nid', pprint=False)
    print('{0} | {1:.2f}  {2:.2f}  {3:.2f} | {4:.2f}  {5:.2f}  {6:.2f}'.format(
        ds.split('/')[1][5:],
        p1, r1, f1, p2, r2, f2))
