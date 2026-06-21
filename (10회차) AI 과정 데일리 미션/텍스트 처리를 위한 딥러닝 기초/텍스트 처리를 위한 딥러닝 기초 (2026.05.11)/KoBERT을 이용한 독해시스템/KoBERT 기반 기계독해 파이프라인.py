import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# 1. KoBERT 모델 및 토커나이저 로드
# MRC 전용 구조(QuestionAnswering) 헤더가 결합된 모델을 불러옵니다.
model_name = "monologg/kobert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# 2. 실습용 지문(Context) 및 질문(Question) 정의
context = """
이순신(李舜臣, 1545년 4월 28일 ~ 1598년 12월 16일)은 조선 중기의 무신이었다.
본관은 덕수, 자는 여해, 시호는 충무이며, 한성 출신이다.
임진왜란 때 조선의 수군을 이끌고 한산도 대첩, 명량 대첩, 노량 대첩 등에서 왜군을 무찔러 승리 가도를 이끌었다.
"""
question = "이순신의 시호는 무엇인가?"

# 3. 입력 데이터 토큰화
# 질문과 본문을 순서대로 넘겨주면 자동으로 [CLS] 질문 [SEP] 본문 [SEP] 구조가 완성됩니다.
inputs = tokenizer(
    question,
    context,
    return_tensors="pt",
    truncation=True,
    max_length=512
)

# 4. 모델 전향 연산 (추론)
with torch.no_grad():
    outputs = model(**inputs)

# outputs 내에는 각 토큰별 start_logits와 end_logits가 포함되어 있습니다.
start_logits = outputs.start_logits
end_logits = outputs.end_logits

# 5. 확률이 가장 높은 시작/끝 토큰 인덱스 추출
# argmax를 통해 본문 텍스트 내에서 가장 높은 스코어를 가진 토큰의 위치를 찾습니다.
start_index = torch.argmax(start_logits).item()
end_index = torch.argmax(end_logits).item() + 1 # 파이썬 슬라이싱 규칙을 위해 +1

# 6. 토큰 ID 배열을 실제 한국어 텍스트 정답으로 복원
predict_tokens = inputs["input_ids"][0][start_index:end_index]
answer = tokenizer.decode(predict_tokens)

print(f"🔮 [질문]: {question}")
print(f"🎯 [모델의 정답 예측]: {answer.strip()}")