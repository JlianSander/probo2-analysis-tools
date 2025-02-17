#!/usr/bin/bash
#set -x

cd probo2-run
eval "$(/home/jsander/tools/miniconda3/bin/conda shell.bash hook)"
conda activate probo2-run
nohup python3 probo2-run.py -m +experiments=$1 > $2
