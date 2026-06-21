import sys
input = sys.stdin.readline

N = int(input())

# 음식의 종류에 따라 개수를 세어야 한다.
# 이때 음식의 종류는 문자열로 주어지며, 음식의 종류마다 개수와 같은 값을 관리해야 하므로
# 맵이 적합한 자료구조다.
info = dict() # 음식의 종류에 따라 개수를 관리하는 맵
for _ in range(N):
	Si, Ai = input().split()
	Ai = int(Ai)

	# 음식의 종류에 따라 개수를 더해준다.
	if Si not in info:
		info[Si] = 0
	info[Si] += Ai

# 음식의 종류에 따라 개수를 전부 구했다면, 음식의 종류를 기준으로 오름차순이 되게 정렬해야 한다.
# 맵을 순회해서 음식의 종류와 개수를 배열에 담아 정렬해서 출력하면 된다.
lst = []
for name, ct in info.items():
	lst.append((name, ct))
lst.sort()

for name, ct in lst:
	print(name, ct)