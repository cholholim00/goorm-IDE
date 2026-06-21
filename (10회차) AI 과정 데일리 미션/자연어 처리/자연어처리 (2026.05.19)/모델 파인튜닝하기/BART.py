import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
from datasets import load_dataset
import evaluate
import numpy as np

# ======================================================
# 1. 환경 설정 및 데이터 전처리
# ======================================================

# 1. 모델 및 토크나이저 로드 (KoBART v2)
model_name = "gogamza/kobart-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 2. 예시 데이터셋 로드 (허깅페이스의 한국어 뉴스 요약 데이터셋 사용)
dataset = load_dataset("daekeun-ml/naver-news-summarization-ko")

max_input_length = 512
max_target_length = 64

def preprocess_function(examples):
    # 인코더 입력: 뉴스 본문 (document)
    inputs = examples['document']
    # 디코더 출력 target: 요약문 (summary)
    targets = examples['summary']

    # 본문 토크나이징
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)

    # 요약문 토크나이징 (text_target 인자 활용)
    labels = tokenizer(text_target=targets, max_length=max_target_length, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# 데이터셋 전체에 전처리 적용
tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# ======================================================
# 2. 평가 지표 및 데이터 콜레이터 설정
# ======================================================

# 3. 데이터 콜레이터 정의 (패딩 및 배치화 담당)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# 4. 평가 지표 정의 (ROUGE Metric)
metric = evaluate.load("rouge")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # 예측 토큰 디코딩
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)

    # 레이블의 패딩 토큰(-100)을 무시하고 디코딩
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # ROUGE 점수 계산
    result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=False)

    # 퍼센트 단위로 변환
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens)

    return {k: round(v * 100, 4) for k, v in result.items()}
# ======================================================
# 3. 트레이너 설정 및 학습 시작
# ======================================================

# 5. 하이퍼파라미터 및 학습 인자 설정
training_args = Seq2SeqTrainingArguments(
    output_dir="./kobart-news-summary",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=4,  # GPU 메모리에 맞게 조절 (OOM 발생 시 2나 1로 축소)
    per_device_eval_batch_size=4,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=3,
    predict_with_generate=True,     # 평가 시 Generate 메서드 강제 사용 (요약 태스크 필수)
    fp16=torch.cuda.is_available(), # GPU 가속 보조
    logging_steps=100,
    load_best_model_at_end=True
)

# 6. Trainer 초기화 및 학습
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# 학습 실행
trainer.train()

# 모델 및 토크나이저 최종 저장
trainer.save_model("./best_kobart_summary_model")

# ======================================================
# 4. 학습된 모델로 뉴스 요약 테스트
# ======================================================

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 저장된 모델과 토크나이저 로드
finetuned_model_path = "./best_kobart_summary_model"
tokenizer = AutoTokenizer.from_pretrained(finetuned_model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(finetuned_model_path)

# GPU 사용 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def summarize_news(text):
    # 토크나이징 및 GPU 이동
    inputs = tokenizer(text, max_length=512, truncation=True, return_tensors="pt").to(device)

    # 추론 (문장 생성)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,          # 빔 서치 크기
        max_length=64,        # 요약문 최대 길이
        min_length=10,        # 요약문 최소 길이
        length_penalty=1.0,   # 길이에 대한 페널티 조정
        no_repeat_ngram_size=3, # 3-gram 중복 생성 방지
        early_stopping=True
    )

    # 디코딩
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 테스트용 뉴스 기사 예시
news_article = """
국내 연구진이 기존보다 충전 속도가 10배 빠른 차세대 배터리 소재를 개발하는 데 성공했습니다.
이번에 개발된 음극재 소재는 전기차에 적용될 경우 완충까지 걸리는 시간을 5분 이내로 단축시킬 수 있을 것으로 기대를 모으고 있습니다.
특히 대량 생산이 용이한 저가형 공정을 기반으로 하여 상용화 가능성이 매우 높다는 평가를 받습니다.
연구팀은 이번 성과가 전기차 보급 가속화와 배터리 시장 판도 변화에 핵심적인 역할을 할 것이라고 밝혔습니다.
"""

print("✨ 원문 뉴스 기사:\n", news_article)
print("-" * 50)
print("🤖 KoBART 요약 결과:\n", summarize_news(news_article))