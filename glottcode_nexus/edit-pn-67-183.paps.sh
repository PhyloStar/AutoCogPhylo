#!/bin/bash
# Job name:
#SBATCH --job-name=edit-pn-67-183.paps
#
# Project:
#SBATCH --account=nn9106k
#
# Wall clock limit:
#SBATCH --time=5:00:00
#
# Max memory usage:
#SBATCH --mem-per-cpu=1G
# Number of tasks (cores):
#SBATCH --ntasks=6
## Set up job environment:
source /cluster/bin/jobsetup
module purge   # clear any inherited modules
set -o errexit # exit on errors
module load intelmpi.intel/5.0.2
cp /usit/abel/u1/tarakark/glottcode_nexus/edit-pn-67-183.paps.mb $SCRATCH
cp /usit/abel/u1/tarakark/glottcode_nexus/edit-pn-67-183.paps.nex $SCRATCH
cp -r /usit/abel/u1/tarakark/mrbayes-coal/mrbayes-3.2.6/ $SCRATCH
chkfile edit-pn-67-183.paps.nex.run1.p edit-pn-67-183.paps.nex.run2.p edit-pn-67-183.paps.nex.run1.t edit-pn-67-183.paps.nex.run2.t edit-pn-67-183.paps.nex.con.tre edit-pn-67-183.papslog.txt
cd $SCRATCH
mpirun -np 6 mrbayes-3.2.6/src/mb edit-pn-67-183.paps.mb > edit-pn-67-183.papslog.txt
