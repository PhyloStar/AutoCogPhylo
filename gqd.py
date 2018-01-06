import itertools as it
import sys, subprocess, glob
import numpy as np
from scipy import stats

cutoff = 0.5

gold_tree = sys.argv[1]
target_fam = sys.argv[2]



 
family = gold_tree.split("/")[1].replace(".glot.tre","")

for tgt in glob.iglob("glottcode_nexus_out/*"+target_fam+"*nwk"):
    gqd = []
    cog_met = tgt.split("/")[-1].split("-")[0].replace("data","")
    if len(cog_met) == 0: cog_met = "gold"
    trees = [x for x in open(tgt, "r")]

    for t1 in trees[int(cutoff*len(trees)):]:
        temp1 = open("temp1.txt", "w")
        temp1.write(t1.replace("_","").replace("-",""))
        temp1.close()
        a = subprocess.check_output(["/home/tarakark/tools/qdist/qdist", "temp1.txt", gold_tree])
        x=str(a).split("\\n")[1].split("\\t")
        gqd.append(float(x[4])/float(x[2]))
    gqd = np.array(gqd)
    print(family, cog_met, np.round(np.mean(gqd),4), np.round(np.std(gqd),4), gqd.shape[0], sep="\t")

