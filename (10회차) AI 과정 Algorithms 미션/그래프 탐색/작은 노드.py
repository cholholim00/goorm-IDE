import sys
from collections import defaultdict
from collections import deque
input = sys.stdin.readline

# 노드의 개수 N, 간선의 개수 M, 시작 노드 K
N, M, K = map(int, input().split())
graph = defaultdict(list)

# 그래프 선언
for _ in range(M):
    s, e = map(int, input().split())
    graph[s].append(e)
    graph[e].append(s)

q = deque()
q.append(K)
# 방문 지점 관리
visited = [False] * (N+1)
visited_cnt  = 1

while q:
    # 현재 노드 추출
    current_Node =q.popleft()
    min_node = N+1
    visited[current_Node] = True
    for i in graph[current_Node]:
        #방문 한 적 없는 노드 중 노드의 번호가 가장 작은 노드만으로 이동함.
        if not visited[i]:
            min_node = min(min_node, i)
    # 더 이상 이동할 노드가 없다면, 이동거리와 마지막 노드를 출력
    if min_node != N+1:
        visited_cnt += 1
        q.append(min_node)
    else:
        print(visited_cnt, current_Node)
        break