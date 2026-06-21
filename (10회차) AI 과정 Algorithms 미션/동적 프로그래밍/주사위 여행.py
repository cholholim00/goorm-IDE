import sys
data = sys.stdin.read().split()
idx = 0
N, M, K = int(data[idx]), int(data[idx+1]), int(data[idx+2]); idx += 3
rest = set()
for _ in range(K):
    r, c = int(data[idx]), int(data[idx+1]); idx += 2
    rest.add((r, c))
MOD = 10**9 + 7
dp = [[0]*(M+1) for _ in range(N+1)]
dp[1][1] = 1
for r in range(1, N+1):
    for c in range(1, M+1):
        if (r,c)==(1,1) or (r,c) in rest: continue
        t = 0
        for x in range(1,7):
            if r-x>=1: t += dp[r-x][c]
            if c-x>=1: t += dp[r][c-x]
        dp[r][c] = t % MOD
print(dp[N][M])