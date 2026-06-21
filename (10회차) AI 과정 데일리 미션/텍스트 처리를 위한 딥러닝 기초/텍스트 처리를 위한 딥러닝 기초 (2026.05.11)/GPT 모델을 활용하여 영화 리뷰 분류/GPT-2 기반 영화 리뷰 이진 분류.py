import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. 모델 및 토커나이저 초기화
model_name = "skt/ko-gpt2-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# GPT-2 필수 설정: 패딩 토큰을 문장 종료(EOS) 토큰으로 지정
tokenizer.pad_token = tokenizer.eos_token

# 이진 분류(긍정/부정)이므로 num_labels=2 설정
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
model.config.pad_token_id = model.config.eos_token_id

# 2. 실습용 가상 영화 리뷰 데이터 (0: 부정, 1: 긍정)
reviews = [
    {"text": "올해 본 영화 중에 가장 가슴이 웅장해지는 최고의 명작.", "label": 1},
    {"text": "돈 주고 보기에는 너무 아깝고 지루함의 연속이었다.", "label": 0},
    {"text": "스토리는 뻔한데 배우들 연기력 덕분에 겨우 끝까지 봄.", "label": 0} # 중립 성향의 부정
]

# 3. 데이터 전처리 및 토큰화
input_texts = [item["text"] for item in reviews]
labels = [item["label"] for item in reviews]

# 문장 끝에 자연스럽게 eos_token이 붙도록 처리한 뒤 토큰화 진행
tokenized_inputs = tokenizer(
    input_texts,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)
tokenized_inputs["labels"] = torch.tensor(labels)

# 4. 모델 추론
model.eval()
with torch.no_grad():
    outputs = model(**tokenized_inputs)
    logits = outputs.logits

    # 이진 분류의 확률 변환 (Softmax 사용)
    probs = torch.softmax(logits, dim=-1)
    predictions = torch.argmax(probs, dim=-1)

# 5. 결과 검증 출력
label_names = ["부정 (Negative)", "긍정 (Positive)"]

print("=== 🎬 네이버 영화 리뷰 감성 분류 결과 ===")
for i, text in enumerate(input_texts):
    pred_idx = predictions[i].item()
    confidence = probs[i][pred_idx].item()

    print(f"\n💬 리뷰: \"{text}\"")
    print(f"🎯 실제 정답: {label_names[labels[i]]}")
    print(f"🔮 모델 예측: {label_names[pred_idx]} (확률: {confidence * 100:.2f}%)")