import sys
import heapq

def solve_move_cost():
    input = sys.stdin.readline
    N = int(input())
    
    # N이 1인 경우 연결할 통로가 없으므로 비용은 0
    if N == 1:
        print(0)
        return

    # MST 방문 여부 체크
    visited = [False] * (N + 1)
    
    # 우선순위 큐: (비용, 목적지 정점)
    # 1번 정점부터 시작한다고 가정
    pq = [(0, 1)]
    
    total_cost = 0
    cnt = 0
    
    while pq:
        cost, curr = heapq.heappop(pq)
        
        # 이미 MST에 포함된 정점이면 건너뜀
        if visited[curr]:
            continue
            
        # MST에 추가
        visited[curr] = True
        total_cost += cost
        cnt += 1
        
        # 모든 정점을 연결했다면 종료
        if cnt == N:
            break
            
        # 현재 정점에서 갈 수 있는 다른 모든 정점과의 간선 비용을 계산하여 큐에 삽입
        # 가중치는 curr * nxt
        for nxt in range(1, N + 1):
            if not visited[nxt] and curr != nxt:
                heapq.heappush(pq, (curr * nxt, nxt))
                
    print(total_cost)

if __name__ == '__main__':
    solve_move_cost()