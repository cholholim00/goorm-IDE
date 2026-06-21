import os
from openai import OpenAI

# API 키 설정 (환경 변수 또는 직접 입력)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))

def call_gpt55(system_instruction: str, user_prompt: str):
    response = client.responses.create(
        model="gpt-5.5",
        messages=[
            {
                "role": "developer", # GPT-5.5 및 최신 Responses API 표준 가이드라인 반영
                "content": system_instruction
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        # 필요 시 추론 모드 제어 (low, medium, high, xhigh)
        # reasoning={"effort": "medium"} 
    )
    return response.message.content

# 💡 시스템 프롬프트 테스트 예시
sys_prompt = "당신은 어려운 의료용어나 기술 문서를 일반인도 쉽게 이해할 수 있도록 명쾌하고 따뜻하게 설명하는 전문 카운셀러입니다."
user_input = "시퀀스 투 시퀀스(Seq2Seq) 모델과 어텐션 메커니즘의 차이를 초등학생도 이해하게 설명해줘."

result = call_gpt55(sys_prompt, user_input)
print("🤖 GPT-5.5 Response:\n", result)