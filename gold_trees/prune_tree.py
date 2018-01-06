from ete3 import Tree
from collections import defaultdict
import sys, glob

exclude_leaves = ["irrr1240"]

for fname in glob.glob("../glottcode_nexus/svm*.nex"):
    family = fname.split("/")[-1].replace("svm-","").replace(".nex","")
    print("Family ", family)
    tree_str = open(sys.argv[1]).read()
    t = Tree(tree_str, format=1)
    leaves_list = []
    for line in open(fname, "r"):
        if "\t" in line:
            leaves_list.append(line.split("\t")[0])
    
    if "aa-" in family:
        leaves_list.remove("irrr1240")
    for leaf in leaves_list:
        if leaf in exclude_leaves:
            print(leaf)
    print(family, leaves_list, len(leaves_list))
    t.prune(leaves_list)

    t.write(format=9, outfile=family+".glot.tre")
