# video-SALMONN 2: Caption-Enhanced Audio-Visual Large Language Models

<div style='display:flex; gap: 0.25rem; '>
<a href='https://arxiv.org/abs/2506.15220'><img src='https://img.shields.io/badge/video_SALMONN_2_paper-PDF-green'></a>
<a href='https://video-salmonn-2.github.io'><img src='https://img.shields.io/badge/Demo-link-green'></a>
<a href='https://huggingface.co/tsinghua-ee/video-SALMONN-2'><img src='https://img.shields.io/badge/video_SALMONN_2_7B-checkpoint-yellow'></a>
<a href='https://huggingface.co/tsinghua-ee/video-SALMONN-2_plus_3B'><img src='https://img.shields.io/badge/video_SALMONN_2+_3B-checkpoint-yellow'></a>
<a href='https://huggingface.co/tsinghua-ee/video-SALMONN-2_plus_7B'><img src='https://img.shields.io/badge/video_SALMONN_2+_7B-checkpoint-yellow'></a>
<a href='https://huggingface.co/tsinghua-ee/video_SALMONN2plus_7B_audioAlign'><img src='https://img.shields.io/badge/video_SALMONN_2+_7B-audioAlign-yellow'></a>
<a href='https://huggingface.co/tsinghua-ee/video-SALMONN-2_plus_72B'><img src='https://img.shields.io/badge/video_SALMONN_2+_72B-checkpoint-yellow'></a>
<a href='https://huggingface.co/datasets/tsinghua-ee/video-SALMONN_2_testset'><img src='https://img.shields.io/badge/video_SALMONN_2-testset-yellow'></a>
</div>


## 🌈 How to Use

### How to train video-SALMONN 2

1. Prepare the dataset following `scripts/example_sft.json` and `scripts/example_dpo.json`.
2. Download LLaVA-OneVision Model from [huggingface](https://huggingface.co/lmms-lab/llava-onevision-qwen2-7b-ov).
3. Modify the parameters in `scripts/train_sft.sh` and `scripts/train_dpo.sh`.
4. Run `bash scripts/train_sft.sh` or `bash scripts/train_dpo.sh`.

### How to evaluate a checkpoint

1. Prepare the dataset following `scripts/example_sft.json`.
2. Modify the parameters in `scripts/eval.sh`.
3. Run `bash scripts/eval.sh`.

### For video-SALMONN 2+, please refer to [video_SALMONN2_plus](https://github.com/bytedance/video-SALMONN-2/tree/main/video_SALMONN2_plus)
