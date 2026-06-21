import sys
input = sys.stdin.readline
from collections import deque

# (si, sj)에서 BFS를 시작해서 방문한 모든 칸의 개수를 출력하는 함수
def bfs(si, sj):
	visited[si][sj] = True # 시작 위치는 방문 처리
	dq = deque()
	dq.append((si, sj)) # 시작 위치를 큐에 담는다.
	sz = 1 # 영역의 크기. 즉, 방문한 칸의 개수

	while dq: # 큐가 비어있다면 종료한다.
		i, j = dq.popleft() # 큐의 맨 앞에 있는 위치를 꺼낸다.
		if 0 <= i - 1 and not visited[i - 1][j] and S[i - 1][j] == '#': # 위
			visited[i - 1][j] = True
			dq.append((i - 1, j))
			sz += 1
		if i + 1 < M and not visited[i + 1][j] and S[i + 1][j] == '#': # 아래
			visited[i + 1][j] = True
			dq.append((i + 1, j))
			sz += 1
		if 0 <= j - 1 and not visited[i][j - 1] and S[i][j - 1] == '#': # 왼쪽
			visited[i][j - 1] = True
			dq.append((i, j - 1))
			sz += 1
		if j + 1 < N and not visited[i][j + 1] and S[i][j + 1] == '#': # 오른쪽
			visited[i][j + 1] = True
			dq.append((i, j + 1))
			sz += 1

	return sz

N, M = map(int, input().split())
S = [input().strip() for _ in range(M)]

# 플러드 필 문제다.
# BFS로 해결할 수 있다.
res = [] # 물체의 크기들을 담아놓는다.
visited = [[False] * N for _ in range(M)]
for i in range(M):
	for j in range(N):
		if visited[i][j] or S[i][j] == '.': # 방문하지 않은 칸이면서 마스킹 처리한 칸을 찾아야 한다.
			continue
		sz = bfs(i, j)
		res.append(sz)

print(len(res)) # 물체의 개수
print(max(res)) # 가장 큰 물체의 크기를 찾아야 한다.