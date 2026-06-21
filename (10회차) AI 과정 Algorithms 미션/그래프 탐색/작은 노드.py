import sys

def solve_smallest_node():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    K = int(data[2])  # 시작 노드 번호
    
    # 인접 리스트 생성
    graph = [[] for _ in range(N + 1)]
    idx = 3
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx+1])
        graph[u].append(v)
        graph[v].append(u)
        idx += 2
        
    # "가장 작은 노드"를 빠르게 찾기 위해 각 인접 리스트를 오름차순으로 정렬
    for i in range(1, N + 1):
        graph[i].sort()

    visited = [False] * (N + 1)
    
    curr = K
    visited[curr] = True
    visited_count = 1  # 시작 노드 포함

    while True:
        next_node = -1
        
        # 이미 정렬되어 있으므로, 방문하지 않은 첫 번째 인접 노드가 가장 번호가 작음
        for neighbor in graph[curr]:
            if not visited[neighbor]:
                next_node = neighbor
                break
        
        # 더 이상 갈 수 있는 미방문 인접 노드가 없다면 탐색 종료
        if next_node == -1:
            break
            
        # 다음 노드로 이동 및 상태 갱신
        visited[next_node] = True
        visited_count += 1
        curr = next_node

    # 결과 출력 (마지막으로 도달한 노드 번호, 방문한 총 노드 수)
    print(curr, visited_count)

if __name__ == '__main__':
    solve_smallest_node()