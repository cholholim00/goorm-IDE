from transformers import AutoModelForSequenceClassification

# 1. NLI 모델 로드 (3개 클래스: 함의, 중립, 모순)
model_model = "klue/bert-base"
nli_model = AutoModelForSequenceClassification.from_pretrained(model_model, num_labels=3)

# 2. 두 문장 쌍 정의 및 토큰화
premise = "두 사람이 자전거를 타고 길을 가고 있다."
hypothesis = "사람들이 야외에서 운동을 하고 있다."

# 토커나이저에 두 문장을 인자로 나란히 넘기면 자동으로 [CLS] 문장1 [SEP] 문장2 [SEP] 구조로 만듭니다.
inputs = tokenizer(premise, hypothesis, return_tensors="pt", truncation=True, padding=True)

# 3. 모델 추론
outputs = nli_model(**inputs)
logits = outputs.logits  # Shape: [batch_size, 3]

# 4. 확률 환산 및 결과 출력
probs = torch.softmax(logits, dim=-1)
predicted_class = torch.argmax(probs, dim=-1).item()

labels = ["함의 (Entailment)", "중립 (Neutral)", "모순 (Contradiction)"]
print(f"예측 결과: {labels[predicted_class]} (확률: {probs[0][predicted_class].item():.4f})")