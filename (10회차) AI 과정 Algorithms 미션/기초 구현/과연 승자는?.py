import sys
input = sys.stdin.readline

N = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

alice = 0
bob = 0
for i in range(N):
	if A[i] == B[i]: # Draw
		alice += 1
		bob += 1
	elif A[i] > B[i]: # Alice > Bob
		if A[i] - B[i] == 7: # dif is 7
			alice -= 1
			bob += 3
		else:
			alice += 2
	else: # Bob > Alice
		if B[i] - A[i] == 7: # dif is 7
			alice += 3
			bob -= 1
		else:
			bob += 2

print(alice, bob)