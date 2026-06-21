import sys
from functools import lru_cache
n, m, k = map(int, sys.stdin.readline().split())
@lru_cache(maxsize=None)
def dp(turn, i, j):
    if i == 0 or j == 0: return 0
    if turn == 0: return 0
    cnt = 0
    if j-1 == 0: cnt += 1
    else: cnt += dp(turn-1, i+1, j-1)
    if i-1 == 0: cnt += 1
    else: cnt += dp(turn-1, i-1, j+1)
    cnt += dp(turn-1, i, j)
    return cnt
print(dp(k, n, m))