import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from transformers import get_linear_schedule_with_warmup

# 1. 간단한 실습용 데이터셋 정의 (리뷰 텍스트와 긍정/부정 라벨)
# 1: 긍정(Positive), 0: 부정(Negative)
train_texts = [
    "이 영화 진짜 강력 추천합니다. 너무 재밌어요!",
    "돈 아까워요.. 보다가 중간에 나왔습니다.",
    "배우들의 연기력이 돋보이는 최고의 작품!",
    "스토리가 너무 뻔하고 지루했습니다."
]
train_labels = [1, 0, 1, 0]

# 2. 토크나이저 및 데이터셋 커스텀 클래스 생성
# BERT는 텍스트를 고유의 서브워드(Subword) 단위로 쪼개고, [CLS], [SEP] 등의 특수 토큰을 붙여 변환합니다.
class SimpleDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=32):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len
        
    def __len__(self):
        return len(self.texts)
        
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # encode_plus는 토큰화, 패딩, 맥스렝스 트렁케이션, 어텐션 마스크 생성을 한 번에 해줍니다.
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True, # [CLS], [SEP] 자동 추가
            max_length=self.max_len,
            padding='max_length',     # 문장 길이를 max_len에 맞춤
            truncation=True,         # 넘치는 길이는 자름
            return_attention_mask=True,
            return_tensors='pt',     # 파이토치 텐서 반환
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

# 3. 환경 설정 및 준비
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"사용 중인 디바이스: {device}")

MODEL_NAME = 'klue/bert-base' # 한국어 대표 BERT 모델
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
model.to(device)

# 데이터로더 생성
train_dataset = SimpleDataset(train_texts, train_labels, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)

# 4. 옵티마이저 및 스케줄러 설정
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
total_steps = len(train_loader) * 3 # 3 에포크 가정
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

# 5. 미세 조정(Fine-tuning) 학습 루프
print("\n--- BERT 모델 학습 시작 ---")
model.train()

for epoch in range(3):
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)
        
        # 모델 예측 및 손실값(Loss) 계산
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # 그래디언트 클리핑으로 안정성 확보
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item()
        
    print(f"Epoch {epoch + 1}/3 | 평균 Loss: {total_loss / len(train_loader):.4f}")

# 6. 추론(Inference) 테스트
print("\n--- 새로운 텍스트 검증 ---")
model.eval()

def predict_sentiment(text):
    with torch.no_grad():
        inputs = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=32,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()
        
        sentiment = "긍정 (Positive)" if prediction == 1 else "부정 (Negative)"
        print(f"입력 문장: '{text}' -> 예측 결과: {sentiment}")

# 테스트 실행
predict_sentiment("이것은 내 인생 최고의 영화다 진짜.")
predict_sentiment("시간 아까우니까 절대 보지 마세요.")