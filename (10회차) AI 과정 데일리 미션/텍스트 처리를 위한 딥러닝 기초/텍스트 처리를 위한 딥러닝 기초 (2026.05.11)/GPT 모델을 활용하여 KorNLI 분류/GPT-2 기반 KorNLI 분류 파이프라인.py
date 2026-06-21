import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. 한국어 GPT-2 모델 및 토커나이저 로드
model_name = "skt/ko-gpt2-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# GPT-2는 기본 패딩 토큰이 없으므로 문장 종료 토큰(EOS)을 PAD 토큰으로 지정합니다.
tokenizer.pad_token = tokenizer.eos_token

# KorNLI의 3가지 클래스(함의, 중립, 모순)를 분류하기 위해 num_labels=3으로 설정
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
model.config.pad_token_id = model.config.eos_token_id

# 2. 실습용 KorNLI 데이터 예시 (전제, 가설, 정답 레이블)
# 클래스 매핑 -> 0: Entailment(함의), 1: Neutral(중립), 2: Contradiction(모순)
sample_data = [
    {
        "premise": "한 남자가 야외 주방에서 요리를 하고 있다.",
        "hypothesis": "한 남자가 밖에서 음식을 만들고 있다.",
        "label": 0  # 함의
    },
    {
        "premise": "의사들이 수술실에서 심각한 표정으로 대화를 나누고 있다.",
        "hypothesis": "의사들이 퇴근 후 회식을 하고 있다.",
        "label": 2  # 모순
    }
]

# 3. 데이터 전처리 및 토큰화 함수
def preprocess_nli_data(data):
    inputs = []
    labels = []

    for item in data:
        # 전제문과 가설문을 결합하여 하나의 시퀀스로 만듭니다.
        # 문장 간의 구분을 위해 두 문장 사이에 공백이나 특수 토큰을 삽입할 수 있습니다.
        text_input = f"{item['premise']} {tokenizer.bos_token} {item['hypothesis']}"
        inputs.append(text_input)
        labels.append(item['label'])

    # 토큰화 진행
    tokenized_inputs = tokenizer(
        inputs,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    tokenized_inputs["labels"] = torch.tensor(labels)
    return tokenized_inputs

# 전처리 실행
batch_inputs = preprocess_nli_data(sample_data)

# 4. 모델 전향 연산 (Forward Pass) 및 손실값 확인
model.train() # 학습 모드 전환
outputs = model(**batch_inputs)

loss = outputs.loss
logits = outputs.logits

print(f"📌 계산된 CrossEntropy Loss: {loss.item():.4f}")
print(f"📌 출력 Logits Shape: {logits.shape} (Batch_size, Num_labels)")

# 5. 추론 및 클래스 예측 결과 출력
model.eval() # 평가 모드 전환
with torch.no_grad():
    inference_outputs = model(**batch_inputs)
    probs = torch.softmax(inference_outputs.logits, dim=-1)
    predictions = torch.argmax(probs, dim=-1)

class_names = ["함의 (Entailment)", "중립 (Neutral)", "모순 (Contradiction)"]

print("\n--- 🔍 예측 결과 검증 ---")
for i, pred_idx in enumerate(predictions.tolist()):
    true_idx = sample_data[i]['label']
    print(f"실제 정답: {class_names[true_idx]}")
    print(f"모델 예측: {class_names[pred_idx]} (확률: {probs[i][pred_idx].item():.4f})\n")