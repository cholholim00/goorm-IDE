import sys
import heapq

def solve_signal():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    grid = [input().strip() for _ in range(N)]
    
    # 8방향 설정 (상, 하, 좌, 우, 좌상, 좌하, 우상, 우하)
    dr = [-1, 1, 0, 0, -1, 1, -1, 1]
    dc = [0, 0, -1, 1, -1, -1, 1, 1]
    
    sr, sc, er, ec = -1, -1, -1, -1
    for r in range(N):
        for c in range(M):
            if grid[r][c] == 'S':
                sr, sc = r, c
            elif grid[r][c] == 'E':
                er, ec = r, c

    # dist[r][c][d]: (r, c) 칸에 d 방향으로 진입했을 때의 최소 시간
    INF = float('inf')
    dist = [[[INF] * 8 for _ in range(M)] for _ in range(N)]
    
    pq = []
    # 시작점 S에서는 8방향 모두로 뻗어나갈 수 있음
    for d in range(8):
        nr, nc = sr + dr[d], sc + dc[d]
        if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] != '#':
            # 다음 칸의 저항력 계산
            if grid[nr][nc] in ('.', 'S', 'E'):
                cost = 1
            else:
                cost = int(grid[nr][nc])
                
            if cost < dist[nr][nc][d]:
                dist[nr][nc][d] = cost
                heapq.heappush(pq, (cost, nr, nc, d))
                
    ans = INF
    
    while pq:
        curr_time, r, c, d = heapq.heappop(pq)
        
        if curr_time > dist[r][c][d]:
            continue
            
        if r == er and c == ec:
            ans = min(ans, curr_time)
            continue
            
        # 다음 이동 방향 결정
        # 현재 칸이 안테나('.')라면 8방향 모두 가능, 숫자라면 기존 방향 d로만 직진
        next_directions = range(8) if grid[r][c] == '.' else [d]
        
        for nd in next_directions:
            nr, nc = r + dr[nd], c + dc[nd]
            if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] != '#':
                if grid[nr][nc] in ('.', 'S', 'E'):
                    weight = 1
                else:
                    weight = int(grid[nr][nc])
                    
                next_time = curr_time + weight
                if next_time < dist[nr][nc][nd]:
                    dist[nr][nc][nd] = next_time
                    heapq.heappush(pq, (next_time, nr, nc, nd))
                    
    print(ans if ans != INF else -1)

if __name__ == '__main__':
    solve_signal()