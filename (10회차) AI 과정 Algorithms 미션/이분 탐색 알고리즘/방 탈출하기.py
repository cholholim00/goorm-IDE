import sys
input = sys.stdin.readline
from bisect import bisect

N = int(input())
A = list(map(int, input().split()))
M = int(input())
B = [int(input()) for _ in range(M)]

# A를 정렬한다.
A.sort()

# Bi가 A에 포함되는지 이분 탐색으로 확인한다.
for i in range(M):
	j = bisect(A, B[i])
	if j and A[j - 1] == B[i]:
		print(1)
	else:
		print(0)