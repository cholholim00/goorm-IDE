import sys
N = int(sys.stdin.readline())
C = list(map(int, sys.stdin.readline().split()))
max_sum = cur = 0
for c in C:
    cur += c
    max_sum = max(max_sum, cur)
    if cur < 0: cur = 0
print(max_sum)