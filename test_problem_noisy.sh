#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=cpu64
#SBATCH --time=23:59:00
#SBATCH --job-name=pytorch_mnist
# #SBATCH --output=qaoa_test.out
 
# Activate environment
# uenv verbose cuda-12.3.2 cudnn-12.x-9.0.0
# uenv verbose cudnn-11.6-8.4.1 cuda-11.6.2 
uenv miniconda3-py310
conda activate qaoa
# Run the Python script that uses the GPU
python -u test_problem_noisy.py $1 $2 $3 # file name, number of layers, number of repetitions

