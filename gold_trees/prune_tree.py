import glob
import re
import sys

from ete3 import Tree

exclude_leaves = ["irrr1240"]
alles = glob.glob("../glottcode_nexus/svm*.nex")
for fname in alles:
    family = fname.split("/")[-1].replace("svm-", "").replace(".nex", "")
    print("Family ", family)
    filename = family.split("\\")[1]
    tree_str = open(sys.argv[1]).read()

    tree_str = re.sub(r':\d', '', tree_str)

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
    all_leaves = [i.name for i in t.get_leaves()]
    for iso in leaves_list:
        if iso not in all_leaves:
            target = t.search_nodes(name=iso)[0]
            target.add_child(name=iso)
            target.name = None
    assert set([i.name for i in t.get_leaves()]) == set(leaves_list)  # everything in leaves list is a leave in the tree
    t.write(format=9, outfile=filename + ".glot_cleaned.tre")
