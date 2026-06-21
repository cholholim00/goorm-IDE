import torch
from sentence_transformers import SentenceTransformer, util

class SBERTChatbot:
    def __init__(self, model_name: str):
        """
        SBERT 기반 챗봇 엔진 초기화
        """
        print(f"🤖 모델 로드 중: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.faq_database = {}
        self.db_questions = []
        self.db_embeddings = None

    def train_database(self, faq_dict: dict):
        """
        질문-답변 딕셔너리를 받아 질문들의 SBERT 임베딩을 미리 계산하여 저장 (인덱싱)
        """
        self.faq_database = faq_dict
        self.db_questions = list(faq_dict.keys())

        # 데이터베이스 내 모든 질문의 벡터 추출 (Tensor 형태로 반환받아 GPU/CPU 연산 준비)
        self.db_embeddings = self.model.encode(
            self.db_questions,
            convert_to_tensor=True,
            show_progress_bar=False
        )
        print(f"✅ {len(self.db_questions)}개의 FAQ 데이터 인덱싱 완료.\n")

    def respond(self, user_question: str, threshold: float = 0.60):
        """
        사용자 질문을 입력받아 가장 유사한 FAQ 답변을 반환
        """
        # 1. 사용자 질문 임베딩 생성
        user_embedding = self.model.encode(user_question, convert_to_tensor=True)

        # 2. 데이터베이스 내 모든 질문 임베딩과의 코사인 유사도 계산
        cosine_scores = util.cos_sim(user_embedding, self.db_embeddings)[0]

        # 3. 가장 유사도가 높은 최적의 매칭 인덱스 추출
        best_match_idx = torch.argmax(cosine_scores).item()
        best_score = cosine_scores[best_match_idx].item()

        # 4. 설정한 임계값(Threshold)을 넘었는지 검증하여 답변 출력
        if best_score >= threshold:
            matched_question = self.db_questions[best_match_idx]
            answer = self.faq_database[matched_question]
            return {
                "status": "success",
                "matched_question": matched_question,
                "answer": answer,
                "score": best_score
            }
        else:
            return {
                "status": "fail",
                "answer": "죄송합니다. 질문의 의도를 정확히 이해하지 못했어요. 다른 표현으로 질문해 주시겠어요?",
                "score": best_score
            }

# ==========================================
# 3. 챗봇 데이터베이스 정의 및 테스트 구동
# ==========================================

# 실습용 샘플 FAQ 데이터 (Medical & General IT 융합 예시)
faq_data = {
    "안구건조증 증상과 예방 대책을 알려주세요.": "안구건조증은 눈이 뻑뻑하고 이물감이 드는 것이 대표적입니다. 인공눈물을 주기적으로 점안하고, 실내 습도를 40~60%로 유지하는 것이 좋습니다.",
    "라식 수술과 라섹 수술의 차이점은 무엇인가요?": "라식은 각막 절편을 만들어 레이저를 조사한 뒤 다시 덮는 방식이고, 라섹은 각막 상피를 얇게 벗겨내어 레이저를 조사하는 방식입니다. 회복 속도와 통증 정도에 차이가 있습니다.",
    "FastAPI 프레임워크에서 비동기 핸들러는 어떻게 선언하나요?": "라우터 함수를 정의할 때 `async def` 키워드를 사용하여 선언하면 비동기 이벤트를 효율적으로 처리할 수 있습니다."
}

# [테스트 1] 멀티태스크 최적화 모델 사용
# 한국어 문장 유사도 및 NLI 다운스트림 태스크에서 범용적으로 우수한 성능을 보이는 모델입니다.
model_v1 = "jhgan/ko-sroberta-multitask"
chatbot_v1 = SBERTChatbot(model_v1)
chatbot_v1.train_database(faq_data)

# [테스트 2] 서울대 연구팀의 경량화 임베딩 모델 사용
# 어휘 및 자막 코퍼스로 학습되어 구어체 대화 질문 매칭에 강점을 가집니다.
model_v2 = "snunlp/KR-SBERT-VCC-lite"
chatbot_v2 = SBERTChatbot(model_v2)
chatbot_v2.train_database(faq_data)


# 4. 실제 사용자 입력 추론 비교
user_inputs = [
    "눈이 너무 뻑뻑하고 모래가 들어간 것 같아요.",
    "FastAPI 비동기 함수 짜는 법 알려줘"
]

print("=== 💬 챗봇 추론 결과 비교 ===")
for user_text in user_inputs:
    print(f"\n🗣️ 사용자 입력: '{user_text}'")

    res_v1 = chatbot_v1.respond(user_text)
    print(f"└ [ko-sroberta] 매칭 질문: {res_v1.get('matched_question', 'N/A')} (Score: {res_v1['score']:.4f})")
    print(f"  답변: {res_v1['answer']}")

    res_v2 = chatbot_v2.respond(user_text)
    print(f"└ [KR-SBERT]   매칭 질문: {res_v2.get('matched_question', 'N/A')} (Score: {res_v2['score']:.4f})")
    print(f"  답변: {res_v2['answer']}")