import sys
N = int(sys.stdin.readline())
MOD = 1_000_000
dp = [[[0]*3 for _ in range(2)] for _ in range(3)]
dp[0][0][0] = 1
dp[1][1][0] = 1
dp[2][0][1] = 1
for _ in range(N-1):
    ndp = [[[0]*3 for _ in range(2)] for _ in range(3)]
    for last in range(3):
        for b in range(2):
            for cs in range(3):
                val = dp[last][b][cs]
                if not val: continue
                ndp[0][b][0] = (ndp[0][b][0] + val) % MOD
                if b == 0:
                    ndp[1][1][0] = (ndp[1][1][0] + val) % MOD
                if cs < 2:
                    ndp[2][b][cs+1] = (ndp[2][b][cs+1] + val) % MOD
    dp = ndp
print(sum(dp[l][b][c] for l in range(3) for b in range(2) for c in range(3)) % MOD)