from lingpy import *
from glob import glob

files = ['ABVD_full.txt', 'IELex-2016.tsv']
for f in files[::-1]:
    print(f)
    lex = LexStat('data/'+f, check=True, transcription='transcription')
    lex.cluster(method='turchin', ref='cogs')
    lex.output('paps.nex', filename=f, ref='cogs', missing='?')
