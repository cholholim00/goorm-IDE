import sys
sys.setrecursionlimit(10**6)

def solve_matjib():
    input = sys.stdin.readline
    N = int(input())
    
    if N == 1:
        print(1)
        return
        
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
        
    # 간선의 개수(거리 1로 취급) 기준 가장 먼 노드 찾기
    def dfs(curr, prev, dist):
        max_node = curr
        max_dist = dist
        
        for nxt in adj[curr]:
            if nxt != prev:
                res_node, res_dist = dfs(nxt, curr, dist + 1)
                if res_dist > max_dist:
                    max_dist = res_dist
                    max_node = res_node
        return max_node, max_dist

    # 1. 1번 정점에서 가장 먼 정점 A 찾기
    A, _ = dfs(1, 0, 0)
    # 2. A 정점에서 가장 먼 정점 B를 찾고 그때의 간선 개수(지름) 구하기
    _, max_edges = dfs(A, 0, 0)
    
    # 정점의 개수는 간선의 개수 + 1
    print(max_edges + 1)

if __name__ == '__main__':
    solve_matjib()