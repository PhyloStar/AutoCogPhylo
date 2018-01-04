import glob
from collections import defaultdict

lang2glottcode = defaultdict()

lines = open("langs_glottocode_list.txt","r").readlines()
for line in lines[1:]:
    l, g = line.replace("\n","").split("\t")
    if len(g) < 1: continue
    lang2glottcode[l] = g


for fname in glob.iglob("nexus/*"):
    #if "paps." not in fname: continue
    idx = 0
    nchar = 0
    print("Processing ", fname)
    lines = open(fname, "r").readlines()
    data = defaultdict()
    for i, line in enumerate(lines):
        if "ntax" in line:
            nchar = int(line.split("=")[-1].replace(";",""))
            #print(nchar)
        if "matrix" in line.lower():
            idx = i
            continue
    
    for line in lines[idx+1:]:
        line = line.replace("\n","")
        line = line.replace(";","")

        if len(line) < 1: continue

        if "end" in line.lower():
            break

        char_idx = len(line) - nchar
        #print(nchar, char_idx)
        if "paps." in fname:
            lang, arr = line[:char_idx].rstrip(), line[char_idx:]
            assert(len(arr) == nchar)
            #print(lang, lang2glottcode[lang], sep="\t") 
        else:
            #print(line)
            lang, arr = line.split("\t")

        if lang in lang2glottcode:
            g = lang2glottcode[lang]
            if g in data:
                print("Language with repeated glottcode ", lang, g)
            else:
                data[g] = arr
        else:
            print("Language not found ", lang)       


    nlangs = len(data.keys())
    print("Final languages= ", nlangs)

    outname = "glottcode_nexus/"+fname.split("/")[-1]
    fw = open(outname,"w")
    fw.write("begin data;"+"\n")
    fw.write("   dimensions ntax="+str(nlangs)+" nchar="+str(nchar)+";\nformat datatype=restriction interleave=no missing= ? gap=-;\nmatrix\n")

    for lang, row in data.items():
        fw.write(lang+"\t"+row+"\n")
    fw.write(";\nend;")

  
