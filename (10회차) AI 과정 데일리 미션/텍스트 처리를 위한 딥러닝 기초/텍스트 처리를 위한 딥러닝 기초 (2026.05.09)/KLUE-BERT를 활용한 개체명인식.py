import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

# 1. 모델 및 토커나이저 로드 (KLUE-BERT-Base)
# NER에서는 예측할 태그 수(num_labels)를 반드시 지정해야 합니다. (예: B-PER, I-PER, O 등)
model_name = "klue/bert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=7)

# 2. 예시 입력 문장 및 토큰화
sentence = "이순신은 조선 시대의 장군이다."
inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)

# 3. 모델 추론
outputs = model(**inputs)
logits = outputs.logits  # Shape: [batch_size, sequence_length, num_labels]

# 4. 예측 결과 추출
predictions = torch.argmax(logits, dim=-1)
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

for token, pred in zip(tokens, predictions[0].tolist()):
    print(f"{token:10s} -> 예측 태그 ID: {pred}")