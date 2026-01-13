# Hallucination Detection for Video-SALMONN-2

이 문서는 비디오와 캡션을 기반으로 주어진 문장이 hallucination인지 판단하는 task를 수행하는 방법을 설명합니다.

## 개요

기존의 단순 캡셔닝 task와 달리, 이 task는:
1. 비디오를 제공
2. 전체 캡션(context)을 제공
3. 특정 문장을 제시하여 이것이 hallucination인지 accurate인지 판단하도록 요청

## 파일 구조

```
video_SALMONN2_plus/
├── 1_run_hallucination_detection.sh          # 추론 실행 스크립트
├── scripts/
│   ├── create_hallucination_dataset.py       # 데이터셋 생성 스크립트
│   ├── evaluate_hallucination_detection.py   # 평가 스크립트
│   └── hallucination_detection_dataset.json  # 생성된 데이터셋
└── output/
    └── hallucination_detection/              # 추론 결과 저장 위치
```

## 사용 방법

### 1. 데이터셋 생성

annotated_captions.json 파일을 기반으로 hallucination detection 데이터셋을 생성합니다:

```bash
cd /data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus

# 기본 설정으로 데이터셋 생성
python3 scripts/create_hallucination_dataset.py

# 커스텀 설정으로 데이터셋 생성
python3 scripts/create_hallucination_dataset.py \
    --annotated_captions /path/to/annotated_captions.json \
    --video_base_path /path/to/video/base \
    --output /path/to/output.json \
    --max_samples 5  # 비디오당 최대 샘플 수 (선택사항)
```

**생성된 데이터셋 통계:**
- 총 샘플: 1,582개
- Accurate: 1,202개 (75.9%)
- Hallucination: 380개 (24.1%)

**모델별 분포:**
- salmonn-7B: 607 samples
- qwen3-vl-8B-thinking: 705 samples
- internVL-30B: 270 samples

각 샘플에는 원본 캡션을 생성한 모델 정보가 포함되어 있어, 어떤 모델이 더 hallucination을 많이 생성하는지 분석할 수 있습니다.

### 2. 추론 실행

생성된 데이터셋으로 hallucination detection 추론을 실행합니다:

```bash
# 기본 실행
bash 1_run_hallucination_detection.sh

# GPU 설정 변경
CUDA_VISIBLE_DEVICES=0 bash 1_run_hallucination_detection.sh
```

**스크립트 파라미터 설명:**
- `--interval 0.1`: 프레임 샘플링 간격
- `--run_name hallucination_detection`: 실험 이름
- `--dataset`: 데이터셋 경로
- `--max_frames 768`: 최대 프레임 수
- `--max_pixels 61250`: 최대 픽셀 수

### 3. 결과 평가

추론이 완료된 후 결과를 평가합니다:

```bash
# 기본 평가
python3 scripts/evaluate_hallucination_detection.py

# 커스텀 평가 (상세 결과 저장)
python3 scripts/evaluate_hallucination_detection.py \
    --dataset scripts/hallucination_detection_dataset.json \
    --predictions output/hallucination_detection/results.json \
    --output output/hallucination_detection/evaluation_results.json
```

**평가 지표:**
- Overall Accuracy: 전체 정확도
- Per-Category Accuracy: 카테고리별 정확도 (accurate vs. hallucination)
- Per-Model Accuracy: 모델별 정확도 (어떤 모델의 캡션이 더 hallucination이 많은지)
- Precision: Hallucination 탐지의 정밀도
- Recall: Hallucination 탐지의 재현율
- F1 Score: Precision과 Recall의 조화 평균

## 데이터셋 형식

각 샘플은 다음과 같은 형식을 갖습니다:

```json
{
  "video": "/path/to/video.mp4",
  "use_audio": true,
  "conversations": [
    {
      "from": "human",
      "value": "<video>\nHere is a caption describing this video:\n\n{전체 캡션}\n\nNow, please determine whether the following statement is accurate or a hallucination based on what you see and hear in the video:\n\nStatement: \"{테스트 문장}\"\n\nIs this statement accurate or a hallucination? Please answer with either 'accurate' or 'hallucination'."
    },
    {
      "from": "gpt",
      "value": "accurate" (또는 "hallucination")
    }
  ],
  "video_id": 1421,
  "model": "salmonn-7B",
  "statement": "테스트 문장",
  "ground_truth": "accurate",
  "original_labels": ["Accurate"]
}
```

## 기존 캡셔닝 task와의 차이점

### 기존 (0_run_inference.sh)
- **Task**: 비디오를 보고 전체 내용을 자세히 설명
- **Input**: 비디오 + 오디오
- **Output**: 긴 형태의 자유로운 설명
- **평가**: BLEU, ROUGE 등의 텍스트 유사도 메트릭

### 새로운 (1_run_hallucination_detection.sh)
- **Task**: 주어진 문장이 비디오 내용과 일치하는지 판단
- **Input**: 비디오 + 오디오 + 캡션 + 테스트 문장
- **Output**: "accurate" 또는 "hallucination"
- **평가**: Accuracy, Precision, Recall, F1 Score

## 주의사항

1. **비디오 파일 경로**: annotated_captions.json의 video_url이 실제 비디오 파일 위치와 일치해야 합니다
2. **메모리 사용량**: max_frames와 max_pixels 설정에 따라 GPU 메모리 사용량이 크게 달라질 수 있습니다
3. **추론 시간**: 비디오 길이와 프레임 수에 따라 추론 시간이 상당히 길어질 수 있습니다

## 문제 해결

### 비디오 파일을 찾을 수 없는 경우
```bash
# 비디오 파일 위치 확인
ls /data1/changbeenkim/videoeval/Video-MME_sampled/

# create_hallucination_dataset.py의 --video_base_path 파라미터 조정
python3 scripts/create_hallucination_dataset.py \
    --video_base_path /correct/path/to/videos
```

### GPU 메모리 부족 시
```bash
# max_frames 또는 max_pixels 값을 줄이기
bash scripts/test.sh \
    --max_frames 512 \
    --max_pixels 40000 \
    ...
```

## 참고

- 원본 annotated_captions.json: `/data1/changbeenkim/video-SALMONN-2/video_SALMONN2_plus/output/test/annotated_captions.json`
- 비디오 파일 위치: `/data1/changbeenkim/videoeval/Video-MME_sampled/{long,medium,short}/`
