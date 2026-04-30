import google.generativeai as genai
import json
import pandas as pd
import re
import time
import sys

# ==========================================
GOOGLE_API_KEY = "AIzaSyCG2HYa10tHOezx9iQ9sVgK5yKIT0pVRKo"

# 공백 제거 안전장치
GOOGLE_API_KEY = GOOGLE_API_KEY.strip()
genai.configure(api_key=GOOGLE_API_KEY)

print("--- [시스템 가동] 사용 가능한 모델을 자동으로 찾습니다 ---")

# ==========================================
# 2. 모델 자동 스캔 (이름 틀릴 걱정 없음)
# ==========================================
def get_auto_model():
    try:
        # 선생님 계정에서 쓸 수 있는 모델 목록을 싹 다 가져옵니다.
        print("📡 구글 서버에서 모델 명단을 받아오는 중...")
        all_models = list(genai.list_models())

        # 그중에서 'generateContent' 기능이 있는 최신 모델 하나를 픽합니다.
        for m in all_models:
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name: # 빠르고 좋은 모델 우선
                    print(f"✅ 찾았습니다! 이 모델을 씁니다: {m.name}")
                    return genai.GenerativeModel(m.name)

        # 못 찾았으면 기본 모델 반환
        return genai.GenerativeModel("gemini-1.5-flash")

    except Exception as e:
        print(f"\n🚨 [치명적 에러] 키가 잘못되었거나, '새 프로젝트'가 아닙니다.")
        print(f"에러 메시지: {e}")
        sys.exit()

# 자동으로 찾은 모델 연결
model = get_auto_model()

# ==========================================
# 3. 데이터 변환 (안전하게 20개 처리)
# ==========================================
def run_etl(text):
    prompt = f"""
    Extract medical data into JSON.
    All values must be in Korean.
    Schema: age(int), gender(str), symptom(str), pain_level(int), duration(str).
    Input: "{text}"
    Output ONLY JSON.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        clean_json = re.sub(r'```json|```', '', text).strip()
        return json.loads(clean_json)
    except:
        return {"error": "Fail"}

# 데이터셋
raw_data = [
    "환자 45세 남성, 어제부터 오른쪽 아랫배가 찢어지게 아픔. 통증 8점.",
    "32세 여성, 편두통 심함.",
    "5살 남자아이, 기침 심하고 열 38.5도.",
    "아 배 아파 죽겠네 진짜.",
    "60세 남성, 가슴 쥐어짜는 통증(10점)."
]

results = []
print(f"\n--- [작업 시작] 5개 샘플 테스트 ---")

for i, text in enumerate(raw_data):
    print(f"[데이터 {i+1}] 변환 중...", end=" ")
    res = run_etl(text)

    if "error" not in res:
        print(f"✅ 성공 -> {res.get('symptom')}")
        results.append(res)
    else:
        print(f"⚠️ 실패 (잠시 대기)")

    time.sleep(2) # 2초 대기

# 저장
if results:
    df = pd.DataFrame(results)
    cols = ["age", "gender", "symptom", "pain_level", "duration"]
    valid_cols = [c for c in cols if c in df.columns]
    if valid_cols:
        df = df[valid_cols]
        print("\n--- [최종 결과] ---")
        display(df) if 'display' in globals() else print(df)
        df.to_csv("medical_final.csv", index=False, encoding="utf-8-sig")