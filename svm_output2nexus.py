import utils
import numpy as np
from collections import defaultdict
import glob

for svm_outf in glob.iglob("svmClustering/results/data-*"):
    print("Processing ", svm_outf)
    binArr = []
    x = defaultdict(lambda: defaultdict(int))
    d = defaultdict(list)

    doc_list, cc_ids = [], []

    f = open(svm_outf, "r")

    header = f.readline().replace("\n","").split("\t")
    doc_idx, svmcc_idx = [header.index(h) for h in ["DOCULECT", "INFERRED_CLASS"]]
    
    for line in f:
        arr = line.split("\t")
        concept = arr[svmcc_idx].split(":")[0]
        x[arr[svmcc_idx]][arr[doc_idx]] = 1

        if arr[doc_idx] not in d[concept]: 
            d[concept].append(arr[doc_idx])

        #print(arr[svmcc_idx], arr[doc_idx])

        if arr[doc_idx] not in doc_list:
            doc_list.append(arr[doc_idx])
    print(doc_list)    

    for clusterID in x:
        temp = []
        concept = clusterID.split(":")[0]
        for doc in doc_list:
            if doc not in d[concept]:
                temp.append("2")
            else:
                temp += [x[clusterID][doc]]
        binArr.append(temp)

    nchar, nlangs = np.array(binArr).shape
    outname = "nexus/svm-"+svm_outf.split("/")[-1].split(".")[0].replace("data-","")
    fw = open(outname+".nex","w")
    fw.write("begin data;"+"\n")
    fw.write("   dimensions ntax="+str(nlangs)+" nchar="+str(nchar)+";\nformat datatype=restriction interleave=no missing= ? gap=-;\nmatrix\n")

    for row, lang in zip(np.array(binArr).T, doc_list):
        rowx = "".join([str(x) for x in row])
        fw.write(lang+"\t"+rowx.replace("2","?")+"\n")
    fw.write(";\nend;")

