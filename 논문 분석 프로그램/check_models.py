import google.generativeai as genai

# 1. 여기에 API 키를 입력하세요
api_key = input("API 키를 입력하세요: ")
genai.configure(api_key=api_key)

print("--------------------------------")
print("사용 가능한 모델 목록:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"목록을 가져오는 중 에러 발생: {e}")
print("--------------------------------")