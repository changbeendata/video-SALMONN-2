#!/bin/bash

# Arnold platform environment variables for local execution
export ARNOLD_WORKER_GPU=1
export ARNOLD_WORKER_NUM=1
export ARNOLD_ID=0

# Master address for local execution
export METIS_WORKER_0_HOST="127.0.0.1"

CUDA_VISIBLE_DEVICES=4 bash scripts/test.sh \
    --interval 0.1 \
    --run_name hallucination_detection \
    --dataset /data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/scripts/hallucination_detection_dataset.json \
    --max_frames 768 \
    --max_pixels 61250 \
    --model /data1/changbeenkim/video-SALMONN-2/models/video_SALMONN2plus_7B_audioAlign \
    --model_base /data1/changbeenkim/video-SALMONN-2/models/video_SALMONN2plus_7B_audioAlign \
    --lora_ckpt /data1/changbeenkim/video-SALMONN-2/models/video-SALMONN-2_plus_7B
