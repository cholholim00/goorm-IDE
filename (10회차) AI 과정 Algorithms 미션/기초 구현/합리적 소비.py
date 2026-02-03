# 1. 물품의 개수 입력 받기
n = int(input())

items = []

# 2. N번 반복하여 물품 이름과 가격 입력 받기
for _ in range(n):
    name, price = input().split()
    # 가격은 숫자이므로 정수형(int)으로 변환
    price = int(price)
    # 리스트에 (이름, 가격) 튜플 형태로 저장
    items.append((name, price))

# 3. 가장 비싼 물품 찾기 (가격인 x[1]을 기준으로 최대값)
most_expensive = max(items, key=lambda x: x[1])

# 4. 가장 저렴한 물품 찾기 (가격인 x[1]을 기준으로 최소값)
cheapest = min(items, key=lambda x: x[1])

# 5. 결과 출력 (문제 요구사항에 맞춰 이름과 가격을 출력)
# 예: 가장 비싼 물품 이름 가격
print(most_expensive[0], most_expensive[1])
# 예: 가장 저렴한 물품 이름 가격
print(cheapest[0], cheapest[1])