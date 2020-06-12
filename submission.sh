#!/bin/bash

#PBS -q batch
#PBS -N outfile_submission
#PBS -M joe_cong1@baylor.edu
#PBS -m be
#PBS -l nodes=1:ppn=2

module load python

cd "$PBS_O_WORKDIR" || exit

python < QCAInputSim.py > outfile_QCAInputSim.out
