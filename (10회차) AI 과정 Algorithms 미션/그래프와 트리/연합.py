import sys
# 재귀 한도 늘리기 (DFS 사용 시 필수)
sys.setrecursionlimit(200000)

def solve_alliance():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    
    # 단방향 간선을 체크하기 위한 인접 리스트나 셋 활용
    # N이 최대 2,000이므로 2차원 배열이나 set 배열을 사용할 수 있습니다.
    edges = [set() for _ in range(N + 1)]
    
    idx = 2
    for _ in range(M):
        s = int(data[idx])
        e = int(data[idx+1])
        edges[s].add(e)
        idx += 2
        
    # 양방향 연결된 간선만 추출하여 새로운 그래프 생성
    graph = [[] for _ in range(N + 1)]
    for u in range(1, N + 1):
        for v in edges[u]:
            # u -> v가 있고, v -> u도 있다면 양방향 연결
            if u in edges[v]:
                graph[u].append(v)

    # 연결 성분 개수(연합 수) 구하기 (DFS)
    visited = [False] * (N + 1)
    
    def dfs(node):
        visited[node] = True
        for nxt in graph[node]:
            if not visited[nxt]:
                dfs(nxt)
                
    alliance_count = 0
    for i in range(1, N + 1):
        if not visited[i]:
            dfs(i)
            alliance_count += 1
            
    print(alliance_count)

if __name__ == '__main__':
    solve_alliance()