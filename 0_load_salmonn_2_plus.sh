#!/bin/bash

huggingface-cli login

huggingface-cli download tsinghua-ee/video_SALMONN2plus_7B_audioAlign \
    --local-dir ./models/video_SALMONN2plus_7B_audioAlign \
    --local-dir-use-symlinks False


huggingface-cli download tsinghua-ee/video-SALMONN-2_plus_7B \
    --local-dir ./models/video-SALMONN-2_plus_7B \
    --local-dir-use-symlinks False