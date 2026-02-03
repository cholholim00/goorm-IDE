N = int(input()) # 땅의 수 입력받음
A = list(map(int, input().split())) # 공백 기준으로 입력 받아 정수로 변환

fence = 2 * N          # 위 + 아래
fence += A[0] + A[-1]  # 왼쪽 + 오른쪽

for i in range(1, N):
    fence += abs(A[i] - A[i - 1])

print(fence)