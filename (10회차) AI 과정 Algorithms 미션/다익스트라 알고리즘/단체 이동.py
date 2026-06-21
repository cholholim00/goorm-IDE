import sys
import heapq

def solve_group_move():
    input = sys.stdin.readline
    
    # N: 방의 개수, M: 통로의 개수
    N, M = map(int, input().split())
    # S: 시작 방, E: 도착 방, C: 사람 수
    S, E, C = map(int, input().split())
    
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u, v, k = map(int, input().split())
        # C명의 사람이 최대 k명씩 나눠서 지나갈 때 필요한 비용 계산
        cost = (C + k - 1) // k
        adj[u].append((v, cost))
        adj[v].append((u, cost))
        
    # 다익스트라 알고리즘 수행
    INF = float('inf')
    dist = [INF] * (N + 1)
    dist[S] = 0
    
    # 우선순위 큐 (비용, 현재 방)
    pq = [(0, S)]
    
    while pq:
        curr_cost, curr = heapq.heappop(pq)
        
        if curr_cost > dist[curr]:
            continue
            
        if curr == E:
            break
            
        for nxt, weight in adj[curr]:
            next_cost = curr_cost + weight
            if next_cost < dist[nxt]:
                dist[nxt] = next_cost
                heapq.heappush(pq, (next_cost, nxt))
                
    if dist[E] == INF:
        print(-1)
    else:
        print(dist[E])

if __name__ == '__main__':
    solve_group_move()