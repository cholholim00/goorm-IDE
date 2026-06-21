import sys
input = sys.stdin.readline
from math import inf
from heapq import heappop, heappush

N, M = map(int, input().split())
S = int(input()) - 1

G = [[] for _ in range(N)]
for _ in range(M):
	s, e, w = map(int, input().split())
	G[s - 1].append((e - 1, w))

# 가중치가 동일하지 않은 그래프에서의 최단 경로는 다익스트라로 풀어내면 된다.
pq = []
heappush(pq, (0, S)) # 시작점과 시작점까지의 비용을 pq에 담는다.
dist = [inf] * N
dist[S] = 0 # 시작점까지의 비용은 0이다.

while pq: # pq가 빌 때까지 반복한다.
	d, u = heappop(pq)
	if dist[u] < d: # 저장된 u까지의 최소 비용이 d가 크다면, 이미 d보다 더 적은 비용으로 u에서 탐색했다는 의미이다.
		continue
	for v, w in G[u]:
		if dist[v] > d + w: # u와 인접한 v까지의 비용보다 u까지의 비용 + 간선의 비용이 더 작다면 v까지의 비용이 갱신될 수 있다.
			dist[v] = d + w
			heappush(pq, (dist[v], v))

res = 0
for i in range(N):
	if dist[i] < inf:
		res += dist[i]
	else:
		res -= 1

print(res)