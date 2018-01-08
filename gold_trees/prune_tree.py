from ete3 import Tree
from collections import defaultdict
import sys, glob
import re

exclude_leaves = ["irrr1240"]
alles = glob.glob("../glottcode_nexus/svm*.nex")
for fname in alles:
    family = fname.split("/")[-1].replace("svm-","").replace(".nex","")
    print("Family ", family)
    filename = family.split("\\")[1]
    tree_str = open(sys.argv[1]).read()

    tree_str = re.sub(r':\d', '',tree_str)
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
    t = Tree(tree_str, format=1)
    t.prune(leaves_list)

    t.write(format=9, outfile=filename+".glot_cleaned.tre")
