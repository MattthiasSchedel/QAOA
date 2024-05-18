#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=cpu64
#SBATCH --time=23:59:00
#SBATCH --job-name=pytorch_mnist
#SBATCH --output=generate_maxcut_$1_$2.out
 
# Activate environment
uenv miniconda3-py310
conda activate qaoa

# Run the Python script that uses the cpu
python -u generate_maxcut.py $1 $2 # number of nodes, number of edges
