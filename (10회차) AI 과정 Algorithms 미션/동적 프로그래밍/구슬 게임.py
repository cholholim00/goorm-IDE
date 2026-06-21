import sys

def solve():
    # 빠른 입출력을 위해 사용합니다.
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    
    # dp[k][i] 배열 초기화 (C++의 dp[1001][201]에 대응하는 크기로 여유 있게 설정)
    # K와 N+M의 범위에 맞춰 Dynamic Programming 테이블을 만듭니다.
    dp = [[0] * (N + M + 2) for _ in range(K + 2)]
    
    # 기저 상태 정의
    dp[0][N] = 1
    
    # DP 점화식 수행
    for k in range(K):
        for i in range(1, N + M):
            if dp[k][i] > 0:  # 불필요한 연산을 줄이기 위한 조건 (생략 가능)
                dp[k+1][i-1] += dp[k][i]
                dp[k+1][i]   += dp[k][i]
                dp[k+1][i+1] += dp[k][i]
                
    # 정답 계산
    answer = 0
    for k in range(K + 1):
        answer += dp[k][0]
        answer += dp[k][N + M]
        
    print(answer)

if __name__ == '__main__':
    solve()