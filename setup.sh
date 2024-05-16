#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=gpuA100 
#SBATCH --time=02:15:00
#SBATCH --job-name=qaoa_setup
#SBATCH --output=qaoa_setup.out
 
# Set up environment
uenv verbose cuda-12.3.2 cudnn-12.x-9.0.0 
uenv miniconda3-py310
coda create -f qiskit_env.yml
