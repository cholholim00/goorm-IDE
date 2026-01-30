# 반복문 (for) - 리스트의 내용을 하나씩 꺼내거나, 특정 횟수만큼 반복할 때 씁니다.
# 리스트 반복
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(f"나는 {fruit}를 좋아해요.")
    
# 횟수 반복
# 0 부터 4까지 출력 (총 5번)
for i in range(5):
    print(f"현재 숫자는 {i}입니다.")

# 조건문 (while) - 특정 조건이 참인 동안 반복할 때 씁니다.
count = 0
while True: # 무한 루프
    count += 1
    print(f"카운트: {count}")
    
    if count == 5:  # 조건을 만족하면 루프 종료
        print("카운트가 5에 도달하여 루프를 종료합니다.")
        break