#!/bin/bash

conda create -n salmon python=3.10 -y
conda activate salmon

pip install -r requirements.txt

pip install torch==2.9.0 torchvision==0.24.0 torchaudio==2.9.0 --index-url https://download.pytorch.org/whl/cu130 # suit with cuda 13.0 installed in server
# conda install -c "nvidia/label/cuda-12.6.3" cuda-nvcc cuda-cudart-dev libcublas-dev libcurand-dev -> is this command works?

conda install conda-forge::ffmpeg # for install torchcodec, video processing
pip install torchcodec

pip install flash-attn==2.7.4.post1 --no-build-isolation # flash attention