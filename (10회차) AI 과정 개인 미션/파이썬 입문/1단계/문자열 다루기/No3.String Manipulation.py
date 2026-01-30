# 문자열 다루기 - 데이터 전처리나 텍스트 분석에서 가장 많이 쓰이는 기능
# 핵심기능
# 1. 자르기: 문자열의 일부분만 가져옵니다.
# 2. 나누기: 특정 문자를 기준으로 리스트로 쪼갭니다.
# 3. 합치기: 리스트를 다시 문자열로 합칩니다.
# 4. 정리하기: 공백을 제거하거나 글자를 바꿉니다.

text = "  안녕하세요 파이썬 입니다."
# 공백 제거
cleaned_text = text.strip()
print("정리된 문자열:", cleaned_text)
# 문자열 교체
fixed_text = cleaned_text.replace("파이썬", "Python")
print("교체된 문자열:", fixed_text)
# 문자열 나누기 - 리스트로 변환
words = fixed_text.split()
print("나누어진 단어들:", words)
# 문자열 합치기 - 리스트를 문자열로 변환
joined_text = " ".join(words)
print("합쳐진 문자열:", joined_text)

