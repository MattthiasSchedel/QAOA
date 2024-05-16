#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=pytorch_mnist
#SBATCH --output=qaoa_test.out
 
# Activate environment
uenv verbose cuda-12.3.2 cudnn-12.x-9.0.0
uenv miniconda3-py310
conda activate qaoa
# Run the Python script that uses the GPU
python -u Simulation.py

