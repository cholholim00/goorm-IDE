W, R = map(int, input().split()) # 공백 기준으로 입력 받아 정수로 변환
# 1RM값
ans = W * (30 + R) // 30 # //으로 인해 소수점 이하는 버리게 된다.
# 결과 출력
print(ans)
