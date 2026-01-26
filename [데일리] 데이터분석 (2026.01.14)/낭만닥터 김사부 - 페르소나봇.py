import google.generativeai as genai

# ==========================================
# 1. 설정 (API 키 입력)
# ==========================================
GOOGLE_API_KEY = "AIzaSyA6eG5oYwYQb8O2hcQTDE4zIYCsSyOz1Gg"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

# ==========================================
# 2. 김사부의 영혼 주입 (Persona Prompt)
# ==========================================
persona_prompt = """
[System Prompt]
너는 돌담병원의 괴짜 천재 의사 '김사부(부용주)'다.
사용자(환자 또는 후배 의사)에게 아래 설정에 맞춰 대답해라.

1. [성격 및 말투]
   - 겉으로는 까칠하고 투박하게 말해라. ("야 이 자식아", "시끄러워" 등 사용)
   - 하지만 속으로는 누구보다 환자의 생명을 중요하게 생각한다.
   - 의학적 지식은 완벽하지만, 권위적이기보다 '실력'과 '책임감'을 강조해라.
   - 말이 길어지면 "집어치워. 팩트만 말해."라고 말을 끊어라.
   - 가끔씩 인생에 대한 깊은 통찰(낭만)이 담긴 조언을 툭 던져라.

2. [핵심 철학]
   - "살린다. 무슨 일이 있어도 살린다."
   - 돈이나 명예보다 사람 목숨이 먼저다.
   - 변명하는 것을 제일 싫어한다.

3. [대화 예시]
   - User: 너무 힘들어서 못 해 먹겠어요.
   - KimSabu: 야, 징징거릴 시간에 환자 바이탈이나 한 번 더 체크해. 의사가 힘들다고 주저앉으면 환자는 누가 지키냐? 그게 네가 말하는 낭만이야?
   - User: 배가 좀 아픈데 괜찮겠죠?
   - KimSabu: 괜찮은지 아닌지 내가 어떻게 알아? 검사도 안 해보고 넘겨짚지 마. 의사는 신이 아니야. 데이터를 믿어. 당장 가서 CT 찍어와!
"""

# 대화 기억 저장소
chat_history = []

# ==========================================
# 3. 챗봇 엔진
# ==========================================
def chat_with_kimsabu(user_input):
    global chat_history

    # ★ 핵심: 김사부 빙의를 위한 강력한 최면(Hidden Instruction)
    hidden_instruction = "\n(System Note: 넌 지금 '김사부'야. 투박하지만 뼈 있는 조언을 해줘. 절대 친절한 AI 말투 쓰지 마.)"

    full_prompt = persona_prompt + "\n\n[이전 대화]\n"
    for chat in chat_history[-4:]:
        full_prompt += f"{chat}\n"

    full_prompt += f"\nUser: {user_input}{hidden_instruction}\nKimSabu:"

    try:
        response = model.generate_content(full_prompt)
        bot_reply = response.text.strip()

        chat_history.append(f"User: {user_input}")
        chat_history.append(f"KimSabu: {bot_reply}")

        return bot_reply
    except Exception as e:
        return f"오류: {str(e)}"

# ==========================================
# 4. 실행
# ==========================================
print("--- [돌담병원 응급실] 김사부가 들어왔습니다. (종료: q) ---")

while True:
    user_q = input("\n[나]: ")
    if user_q.lower() == '이제 퇴원 해보겠습니다':
        print("[김사부]: 그래, 갈 거면 빨리 가. 응급실 바빠.")
        break

    answer = chat_with_kimsabu(user_q)
    print(f"[김사부]: {answer}")