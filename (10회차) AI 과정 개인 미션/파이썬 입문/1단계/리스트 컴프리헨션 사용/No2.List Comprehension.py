# 리스트 컴프리헨션 - 리스트를 더 짧고 간결하게 만드는 파이썬만의 강력한 문법입니다.
# 기본 공식: [표현식 for 항목 in 반복가능객체 if 조건문]

number = [1, 2, 3, 4, 5]

# [일반적인 for문]
result = []
for n in number:
    if n in number:
        result.append(n * 2)
        
# 리스트 컴프리헨션으로 변환
result_comp = [n * 2 for n in number]
print(result_comp)  # 출력: [2, 4, 6, 8, 10]

# 조건문이 포함된 리스트 컴프리헨션
# 1부터 10까지의 수 중에서 짝수의 제곱을 구하는 예제
evens_squared = [x**2 for x in range(1, 11) if x % 2 == 0]
print(evens_squared)  # 출력: [4, 16, 36, 64, 100]
