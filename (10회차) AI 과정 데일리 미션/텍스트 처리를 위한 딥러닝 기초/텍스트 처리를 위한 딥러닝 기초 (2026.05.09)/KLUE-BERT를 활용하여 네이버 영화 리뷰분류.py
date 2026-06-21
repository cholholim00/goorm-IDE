# 1. 감성 분류 모델 로드 (이진 분류이므로 num_labels=2)
review_model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 2. 리뷰 데이터 토큰화
review = "이 영화 진짜 시간 가는 줄 모르고 봤습니다. 강추!"
inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)

# 3. 모델 추론
outputs = review_model(**inputs)
logits = outputs.logits  # Shape: [batch_size, 2]

# 4. 결과 출력
probs = torch.softmax(logits, dim=-1)
predicted_class = torch.argmax(probs, dim=-1).item()

review_labels = ["부정 (Negative)", "긍정 (Positive)"]
print(f"리뷰 감성 분석 결과: {review_labels[predicted_class]} (확률: {probs[0][predicted_class].item():.4f})")