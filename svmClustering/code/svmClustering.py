# -*- coding: utf-8 -*-
from numpy import *
import pandas as pd
import lingpy as lp
import re
import numpy.random as nprandom
import igraph
import random
igraph.set_random_number_generator(random)
from lingpy.algorithm.extra import infomap_clustering
from Bio import pairwise2
from scipy import stats
from lingpy.basic.wordlist import Wordlist
from sklearn import svm
from lingpy.evaluate.acd import bcubes
import sys

dataset = '.'.join(sys.argv[1].split('.')[:-1])

f = open('sounds41.txt')
sounds = array([x.strip() for x in f.readlines()])
f.close()


f = open('pmi-world.txt','r')
l = f.readlines()
f.close()
logOdds = array([x.strip().split() for x in l],double)

lodict = dict()
for i in xrange(len(sounds)):
    for j in xrange(len(sounds)):
        lodict[sounds[i],sounds[j]] = logOdds[i,j]

f = open('gapPenalties.txt')
gp1,gp2 = array([x.strip() for x in f.readlines()],double)
f.close()


lp.rc(schema='ipa')

def nwBio(x,y,lodict=lodict,gp1=gp1,gp2=gp2):
    al = pairwise2.align.globalds(x,y,lodict,gp1,gp2)[0]
    return al[2],array(al[:2])



data = pd.read_table('../data/'+dataset+'.tsv',sep='\t',
                     encoding='utf-8',na_filter=False)



def cleanASJP(word):
    word = word.replace('\t','')
    word = word.replace(' ','')
    word = word.replace(',','-')
    word = word.replace('%','-')
    word = re.sub(r"(.)(.)(.)\$",r"\2",word)
    word = word.replace('*','')
    word = word.replace('\"','')
    word = re.sub(r".~","",word)
    word = re.sub("-+","-",word)
    word = word.strip('-')
    return word


# lingpy IPA-to-ASJP converter plus some cleanup
# -*- coding: utf-8 -*-
def toASJP(w):
    if w == u'ũ': return 'u'
    if w == u'XXX': return ''
    w = w.replace('\"','').replace('-','')#.replace(' ','')
    wA = ''.join(lp.tokens2class(w.split(),'asjp'))
    wAA = cleanASJP(wA.replace(u'0','').replace(u'I',u'3').replace(u'H',u'N'))
    return ''.join([x for x in wAA if x in sounds])


data['ASJP1'] = [toASJP(w) for w in data.TOKENS.values]



new_data = {}  # the data formatted as LexStat wants it
new_data[0] = ['doculect', 'concept', 'ipa', 'tokens', 'index']  # header
key = 1
for i in data.index:
    nl = list(data.ix[i][['DOCULECT','CONCEPT','FORM']])
    nl.append(data.ix[i]['TOKENS'].split())
    nl.append(i)
    new_data[key] = nl
    key += 1

wl = lp.Wordlist(new_data)


lex = lp.LexStat(wl)
lex.get_scorer(runs=10000, preprocessing=False)




def get_pairs(lang1, lang2, lex):
    """
    Returns all the lang1-lang2 pairs of words with the same Concepticon ID.
    Returns [] of LexStat ID tuples.
    
    Note that LexStat.pairs cannot be used here because the latter flattens
    transcription duplicates.
    """
    pairs = []
    for gloss1, indices1 in lex.get_dict(col=lang1).items():
        for gloss2, indices2 in lex.get_dict(col=lang2).items():
            if gloss1 == gloss2:
                pairs.extend([
                    (i, j) for i in indices1 for j in indices2
                    ])
    return pairs


taxa = data.DOCULECT.unique()

def lexstatSims(lex,taxa=taxa):
    output = {}
    for l1 in taxa:
        for l2 in taxa:
            if l1<l2:
                for p1,p2 in get_pairs(l1,l2,lex):
                    aa = lex.align_pairs(p1, p1, pprint=False, distance=False)[2]
                    ab = lex.align_pairs(p1, p2, pprint=False, distance=False)[2]
                    bb = lex.align_pairs(p2, p2, pprint=False, distance=False)[2]
                    lsSim = 1.-((2*ab)/(aa+bb))
                    output[p1,p2]=lsSim
    return output



lsSims = lexstatSims(lex)


def pValue(x,offDiag):
    return (1.+sum(offDiag>x))/(1.+len(offDiag))


def computePMI(l1,l2,data):
    wl1 = data[data.DOCULECT==l1][['CONCEPT','DOCULECT','ASJP1']].copy()
    wl1['ID'] = wl1.index
    wl2 = data[data.DOCULECT==l2][['CONCEPT','DOCULECT','ASJP1']].copy()
    wl2['ID'] = wl2.index

    wpairs = pd.DataFrame([(l1,c1,w1,id1,l2,c2,w2,id2,nwBio(w1,w2)[0])
                           for (c1,l1,w1,id1) in wl1.values
                           for (c2,l2,w2,id2) in wl2.values],
                          columns = ['l1','c1','w1','id1',
                                     'l2','c2','w2','id2',
                                     'pmi'])
    offDiagonal = wpairs[wpairs.c1!=wpairs.c2]['pmi'].values
    mu,sigma = mean(offDiagonal),std(offDiagonal)

    dg = wpairs[wpairs.c1==wpairs.c2][['c1','l1','w1','id1',
                                         'l2','w2','id2','pmi']].copy()

    dg['calib'] = [-log(pValue(x,offDiagonal)) for x in dg.pmi.values]
    dg['ldist'] = dg.calib.mean()
    return dg

vectors = pd.DataFrame(columns=['c1', 'l1', 'w1', 'id1',
                                'l2', 'w2', 'id2', 'pmi', 'calib', 'ldist'])
for i,l1 in enumerate(taxa):
    print round(1-(1-float(i)/len(taxa))**2,3)
    for j,l2 in enumerate(taxa):
        if i<j:
            vectors = pd.concat([vectors,computePMI(l1,l2,data)])

for i,j in lsSims.keys():
    lsSims[j,i] = lsSims[i,j]

vectors['LexStat'] = [lsSims[int(i+1),int(j+1)]
                      for i,j in vectors[['id1','id2']].values]


wlength = data.groupby('CONCEPT').apply(lambda x:mean(map(len,x.ASJP.values)))

corr = vectors.groupby('c1').apply(lambda x:corrcoef(x.calib,x.ldist)[0,1])


vectors['wLength'] = [wlength[c] for c in vectors.c1.values]
vectors['corr'] = [corr[c] for c in vectors.c1.values]

vectors['feature1'] = vectors['pmi']
vectors['feature4'] = vectors['ldist']
vectors['feature6'] = vectors['wLength']
vectors['feature7'] = vectors['corr']
vectors['feature8'] = vectors['LexStat']

dDict = {'gloss':unicode,
         'l1':unicode,
         'w1':unicode,
         'cc1':unicode,
         'l2':unicode,
         'w2':unicode,
         'cc2':unicode,
         'feature1':double,
         'feature2':double,
         'feature3':double,
         'feature4':double,
         'feature5':double,
         'lexstat_simAA':double,
         'lexstat_simBB':double,
         'lexstat_simAB':double,
         'feature7':double,
         'target':int,
         'db':unicode}




training = pd.read_csv('trainingData.csv',encoding='utf-8',dtype=dDict)


training['feature8'] = 1-((2*training.lexstat_simAB)/(training.lexstat_simAA+training.lexstat_simBB))


training = training[training.db!='Lolo-Burmese']
training = training[training.db!='Bai-110-09']
training = training[training.db!='Chinese-140-15']
training = training[training.db!='Chinese-180-18']
training = training[training.db!='Tujia-109-5']




features = [
    'feature1',
    'feature4',
    'feature6',
    'feature7',
    'feature8',
    ]

nprandom.seed(1234)
random.seed(1234)
trainingVectors = training.ix[nprandom.permutation(training.index)[:7000]]

featureSubset=features
C=0.82
gamma=9e-04
kernel='linear'
th=.34


newWordList = pd.DataFrame()
fitting = trainingVectors
validation = vectors.copy()
X = fitting[featureSubset].values
y = fitting.target.values
svClf = svm.SVC(kernel=kernel,C=C,gamma=gamma,
                probability=True)
svClf.fit(X,y)
svScores = svClf.predict_proba(validation[featureSubset].values)[:,1]
validation['svScores'] = svScores
scores = pd.DataFrame()
wordlist = pd.DataFrame()
concepts = validation.c1.unique()
taxa = unique(validation[['l1','l2']].values.flatten())

dataWordlist = vstack([validation[['c1','l1','w1','id1']].values,
                       validation[['c1','l2','w2','id2']].values])

dataWordlist = pd.DataFrame(dataWordlist,columns=['concept','doculect',
                                                  'counterpart','id'])

dataWordlist = dataWordlist.drop_duplicates()
dataWordlist.index = dataWordlist.id.values

for c in concepts:
    dataC= validation[validation.c1==c].copy()
    wlC = dataWordlist[dataWordlist.concept==c].copy()
    if len(wlC)>1:
        svMtx = zeros((len(wlC.index),len(wlC.index)))
        svMtx[pd.match(dataC.id1,wlC.index),
                 pd.match(dataC.id2,wlC.index)] = dataC.svScores.values
        svMtx[pd.match(dataC.id2,wlC.index),
                 pd.match(dataC.id1,wlC.index)] = dataC.svScores.values
        svDistMtx = log(1-svMtx)
        tth = log(th)-svDistMtx.min()
        svDistMtx -= svDistMtx.min()
        fill_diagonal(svDistMtx,0)
        pDict = infomap_clustering(tth,svDistMtx)
        pArray = vstack([c_[pDict[k],[k]*len(pDict[k])] for k in pDict.keys()])
        partitionIM = pArray[argsort(pArray[:,0]),1]
    else:
        partitionIM = array([1])
    wlC['svmCC'] = [c+':'+str(x) for x in partitionIM]
    newWordList = pd.concat([newWordList,wlC])

data['id'] = data.index


inferredData = pd.merge(data,newWordList[['id','svmCC']])


lex.cluster(method='lexstat',threshold=0.57,
            external_function=lambda x, y: infomap_clustering(y, x, revert=True),
            ref="lexstat_infomap")

partition = vstack([array([concatenate(lex.get_dict(col=l,entry=entry).values())
                           for entry in ['lexstat_infomap','index']]).T for l in taxa])


partition = pd.DataFrame(partition,columns=['lpCC','id'])


inferredData = pd.merge(inferredData,partition)




inferredData.to_csv('../results/'+dataset+'.clustered.tsv',
                    sep='\t',
                    encoding='utf-8',index=False)



clustered = lp.Wordlist('../results/'+dataset+'.clustered.tsv')


with open('../results/f-scores.csv','a') as f:
    lsFscores = bcubes(clustered,gold='COGID',test='lpcc')
    f.write(dataset+',LexStat,'+','.join(map(str,around(array(lsFscores),3)))+'\n')
    svmFscores = bcubes(clustered,gold='COGID',test='svmcc')
    f.write(dataset+',SVM,'+','.join(map(str,around(array(svmFscores),3)))+'\n')
