from collections import defaultdict
import itertools
import numpy as np

def cleanASJP(w):
    w = w.replace("%","")
    w = w.replace("K","k")
    w = w.replace("~","")
    w = w.replace("*","")
    w = w.replace("\"","")
    w = w.replace("$","")
    return w

def writeNexus(dm,f):
    l=len(dm)
    f.write("#nexus\n"+
                  "\n")
    f.write("BEGIN Taxa;\n")
    f.write("DIMENSIONS ntax="+str(l)+";\n"
                "TAXLABELS\n"+
                "\n")
    i=0
    for ka in dm:
        f.write("["+str(i+1)+"] '"+ka+"'\n")
        i=i+1
    f.write(";\n"+
               "\n"+
               "END; [Taxa]\n"+
               "\n")
    f.write("BEGIN Distances;\n"
            "DIMENSIONS ntax="+str(l)+";\n"+
            "FORMAT labels=left;\n")
    f.write("MATRIX\n")
    i=0
    for ka in dm:
        row="["+str(i+1)+"]\t'"+ka+"'\t"
        for kb in dm:
            row=row+str(dm[ka][kb])+"\t"
        f.write(row+"\n")
    f.write(";\n"+
    "END; [Distances]\n"+
    "\n"+
    "BEGIN st_Assumptions;\n"+
    "    disttransform=NJ;\n"+
    "    splitstransform=EqualAngle;\n"+
    "    SplitsPostProcess filter=dimension value=4;\n"+
    "    autolayoutnodelabels;\n"+
        "END; [st_Assumptions]\n")
    f.flush()

def dict2binarynexus(d, lang_list):
    binArr = []
    x = defaultdict(lambda: defaultdict(int))
    LANGS = []
    for langID, clusterID in d.items():
        if langID[1] not in LANGS: LANGS.append(langID[1])
        x[clusterID][langID[1]] = 1

    for clusterID in x.keys():
        temp = []
        for lang in lang_list:
            if lang not in LANGS: temp.append(2)
            else:
                temp += [x[clusterID][lang]]
        binArr.append(temp)
    return binArr
    
    


