# 테스트 케이스 개수 입력
T = int(input())
# 조건 만족 개수 저장할 변수
count = 0 

# T번 반복
for _ in range(T):
    A, B = map(int, input().split()) # 두 수 입력 받기

	# 큰 수/작은 수 구분  
    big = max(A, B) 
    small = min(A, B)

	# 여유 황금비 조건 검사 
    if 1.6 * small <= big <= 1.63 * small:
        count += 1 # 조건 만족하면 개수+1

print(count)