import sys
N = int(sys.stdin.readline())
MOD = 100_000_007
valid = [s for s in range(8) if not ((s & 3) == 3 or (s >> 1 & 3) == 3)]
dp = {s: 1 for s in valid}
for _ in range(N-1):
    ndp = {s: 0 for s in valid}
    for prev in valid:
        for cur in valid:
            if not (prev & cur):
                ndp[cur] = (ndp[cur] + dp[prev]) % MOD
    dp = ndp
print(sum(dp.values()) % MOD)