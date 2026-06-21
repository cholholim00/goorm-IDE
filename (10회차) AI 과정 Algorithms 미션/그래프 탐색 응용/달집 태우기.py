import sys
sys.setrecursionlimit(10**6)

def solve_daljib():
    input = sys.stdin.readline
    N = int(input())
    if N == 1:
        print(0)
        return
        
    adj = [[] for _ in range(N + 1)]
    for i in range(1, N):
        # i+1번 정점이 Ai번 정점과 길이 Li 간선으로 연결됨
        a, l = map(int, input().split())
        adj[a].append((i + 1, l))
        adj[i + 1].append((a, l))
        
    # 가장 먼 노드와 거리를 구하는 DFS (경로 추적 포함)
    def dfs(curr, prev, dist, path_tracker):
        max_node = curr
        max_dist = dist
        
        for nxt, weight in adj[curr]:
            if nxt != prev:
                path_tracker[nxt] = curr
                res_node, res_dist = dfs(nxt, curr, dist + weight, path_tracker)
                if res_dist > max_dist:
                    max_dist = res_dist
                    max_node = res_node
        return max_node, max_dist

    # 1. 임의의 1번 노드에서 가장 먼 노드 X 찾기
    tracker1 = {}
    X, _ = dfs(1, 0, 0, tracker1)
    
    # 2. X에서 가장 먼 노드 Y 찾기 (트리의 지름 경로 확보)
    tracker2 = {X: 0}
    Y, total_diameter = dfs(X, 0, 0, tracker2)
    
    # 3. X부터 Y까지의 경로 리스트 추출
    path = []
    curr = Y
    while curr != 0:
        path.append(curr)
        curr = tracker2.get(curr, 0)
    path.reverse()  # X -> ... -> Y 순서로 정렬
    
    # 4. 경로 위의 각 노드들이 X로부터 떨어진 누적 거리 계산
    # 각 간선의 길이를 구하기 위해 가중치를 다시 매핑해 줍니다.
    # 단, 입력 구조상 트리 가중치 조회를 빠르게 하기 위해 딕셔너리 형태로 저장해둡니다.
    dist_from_X = [0] * len(path)
    
    # 간단하게 X로부터의 거리를 구하기 위해 한번 더 가벼운 DFS를 돌리거나
    # 트리의 특성을 이용해 누적 거리를 채웁니다.
    # 여기서는 다시 한 번 X에서 출발하는 거리만 계산합니다.
    visited_dist = {X: 0}
    def get_all_dist(curr, prev, dist):
        for nxt, weight in adj[curr]:
            if nxt != prev:
                visited_dist[nxt] = dist + weight
                get_all_dist(nxt, curr, dist + weight)
                
    get_all_dist(X, 0, 0)
    
    # 지름 경로 상의 노드들 중, max(X까지 거리, Y까지 거리)가 최소가 되는 값 찾기
    min_max_time = float('inf')
    for node in path:
        d1 = visited_dist[node]            # X까지의 거리
        d2 = total_diameter - d1           # Y까지의 거리
        current_max = max(d1, d2)
        if current_max < min_max_time:
            min_max_time = current_max
            
    print(min_max_time)

if __name__ == '__main__':
    solve_daljib()