#!/bin/bash
#SBATCH --gres=gpu:0
#SBATCH --partition=gpuA100
#SBATCH --time=02:15:00
#SBATCH --job-name=qaoa_setup
#SBATCH --output=qaoa_setup.out

# Set up environment
uenv verbose cuda-12.3.2 cudnn-12.x-9.0.0 
uenv miniconda3-py310

# Create conda environment
conda create -n qaoa -y

# Activate conda environment
source activate qaoa

# Install packages
conda install -c conda-forge qiskit qiskit-optimization scipy matplotlib numpy networkx -y

# Install qiskit-aer with GPU support
pip install qiskit-aer-gpu
