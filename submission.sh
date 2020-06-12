#!/bin/bash

#PBS -q batch
#PBS -N outfile_submission
#PBS -M joe_cong1@baylor.edu
#PBS -m be
#PBS -l nodes=1:ppn=1

module load python/3.7.0

cd $PBS_O_WORKDIR

python < QCA-sub-script.py > outfile_submission.pyout
