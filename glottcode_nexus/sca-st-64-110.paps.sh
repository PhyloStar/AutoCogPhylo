#!/bin/bash
# Job name:
#SBATCH --job-name=sca-st-64-110.paps
#
# Project:
#SBATCH --account=nn9106k
#
# Wall clock limit:
#SBATCH --time=12:00:00
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
cp /usit/abel/u1/tarakark/glottcode_nexus/sca-st-64-110.paps.mb $SCRATCH
cp /usit/abel/u1/tarakark/glottcode_nexus/sca-st-64-110.paps.nex $SCRATCH
cp -r /usit/abel/u1/tarakark/mrbayes-coal/mrbayes-3.2.6/ $SCRATCH
chkfile sca-st-64-110.paps.nex.run1.p sca-st-64-110.paps.nex.run2.p sca-st-64-110.paps.nex.run1.t sca-st-64-110.paps.nex.run2.t sca-st-64-110.paps.nex.con.tre sca-st-64-110.papslog.txt
cd $SCRATCH
mpirun -np 6 mrbayes-3.2.6/src/mb sca-st-64-110.paps.mb > sca-st-64-110.papslog.txt
