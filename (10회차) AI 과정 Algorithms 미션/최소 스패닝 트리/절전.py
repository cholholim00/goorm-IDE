import sys
input = sys.stdin.readline
from heapq import heappop, heappush

''' 1번 구역을 포함해서 K개의 구역이 연결되게끔 최소한의 비용을 들여서 간선을 추가해야 한다.
이는 최소 스패닝 트리를 구하는 문제다.
1번 구역부터 최소 스패닝 트리를 확장시켜야 하므로 프림이 적합하다. '''

N, M, K = map(int, input().split())
G = [[] for _ in range(N)]
tot = 0 # 모든 복도의 소비 전력의 합
for _ in range(M):
	a, b, c = map(int, input().split())
	a -= 1
	b -= 1
	G[a].append((b, c))
	G[b].append((a, c))
	tot += c

# 우선순위 큐를 이용해 현재 연결된 정점으로부터 나아가는 간선들 중 가중치가 가장 낮은 간선을 뽑아야 한다.
pq = [(0, 0)] # 1번 구역부터 시작해야 한다.
ct = 0 # 현재 최소 스패닝 트리의 크기
res = 0 # 최소 스패닝 트리를 이루는 간선들의 가중치의 합
visited = [False] * N

while ct < K: # 크기가 K가 될 때까지 반복해야 한다.
	d, a = heappop(pq)

	# 방문하지 않은 정점으로 나아가는 간선이 뽑혔다면 추가해준다.
	if visited[a]:
		continue
	visited[a] = True
	ct += 1
	res += d

	# 그 정점에서 다시 나아가는 간선을 우선순위 큐에 넣는다.
	for b, c in G[a]:
		if visited[b]:
			continue
		heappush(pq, (c, b))

# 최소한으로 드는 소비 전력을 총 소비 전력에서 빼주면 된다.
print(tot - res)