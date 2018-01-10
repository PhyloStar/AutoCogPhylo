import glob


















##module load openmpi.gnu/1.8.8


## Copy input files to the work directory:



## Make sure the results are copied back to the submit directory (see Work Directory below):


## Do some work:

#YourCommands



for fname in glob.glob("glottcode_nexus/*nex"):
    outname = fname.replace(".nex","")+".sh"
    generic_name = fname.split("/")[-1].replace(".nex","")
    fw = open(outname, "w")
    print("#!/bin/bash","# Job name:","#SBATCH --job-name="+generic_name, "#","# Project:","#SBATCH --account=nn9106k", "#", "# Wall clock limit:", "#SBATCH --time=12:00:00", "#", "# Max memory usage:","#SBATCH --mem-per-cpu=1G", "# Number of tasks (cores):", "#SBATCH --ntasks=6", "## Set up job environment:", "source /cluster/bin/jobsetup", "module purge   # clear any inherited modules", "set -o errexit # exit on errors", "module load intelmpi.intel/5.0.2", sep="\n", file=fw)
    print("cp /usit/abel/u1/tarakark/glottcode_nexus/"+generic_name+".mb $SCRATCH", file=fw)
    print("cp /usit/abel/u1/tarakark/glottcode_nexus/"+generic_name+".nex $SCRATCH", file=fw)
    print("cp -r /usit/abel/u1/tarakark/mrbayes-coal/mrbayes-3.2.6/ $SCRATCH", file=fw)
    print("chkfile "+generic_name+".nex.run1.p "+ generic_name+".nex.run2.p "+ generic_name+".nex.run1.t "+ generic_name+".nex.run2.t "+ generic_name+".nex.con.tre "+ generic_name+"log.txt", file=fw)
    print("cd $SCRATCH", file=fw)
    print("mpirun -np 6 mrbayes-3.2.6/src/mb "+generic_name+".mb > "+generic_name+"log.txt", file=fw) 
    fw.close()



