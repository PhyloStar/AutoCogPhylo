import glob


for fname in glob.glob("glottcode_nexus/*nex"):
    outname = fname.replace(".nex","")+".mb"
    fw = open(outname, "w")
    print("execute "+fname.split("/")[-1]+";", "prset brlenspr = clock:uniform;",  "prset clockvarpr = igr;", "lset coding=noabsencesites rates=gamma;", "mcmcp ngen=8000000 samplefreq=1000 nruns=2 nchains=3;", "mcmc;", "sump;", "sumt;", file=fw,  sep="\n")
    fw.close()
    
