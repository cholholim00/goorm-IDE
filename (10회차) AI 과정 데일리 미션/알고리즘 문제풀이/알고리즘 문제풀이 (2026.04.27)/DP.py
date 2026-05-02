# 다이나믹 프로그래밍
# 재귀적 DP : 이항계수 
def binomial_top_down(n, k, memo):
    # 기본 케이스
    if k == 0 or k == n:
        return 1
    
    # 메모이제이션(이미 계산된 결과가 있으면 반환)
    if memo[n][k] != -1:
        return memo[n][k]
    
    # 재귀 단계: n-1개에서 k-1개를 선택하는 경우 + n-1개에서 k개를 선택하는 경우
    # 계산된 결과를 메모이제이션 딕셔너리에 저장
    memo[n][k] = binomial_top_down(n - 1, k - 1, memo) + binomial_top_down(n - 1, k, memo)
    return memo[n][k]

# 실행
N, K = 5, 2
memo_table = [[-1] * (K + 1) for _ in range(N + 1)]
print(f"{N}C{K} = {binomial_top_down(N, K, memo_table)}")  # 결과: 10