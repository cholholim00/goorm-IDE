import sys
from collections import deque

def solve_fire():
    # 빠른 입력을 위해 사용 (백준/정올 등에서 유용)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    R = int(data[0])
    C = int(data[1])
    
    grid = []
    idx = 2
    for _ in range(R):
        grid.append(data[idx])
        idx += 1

    # 불이 도달하는 시간을 기록할 배열 (-1은 미방문)
    fire_time = [[-1] * C for _ in range(R)]
    queue = deque()
    
    cloud_r, cloud_c = -1, -1

    # 초기 불 위치와 구름이 위치 탐색
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '@':
                queue.append((r, c))
                fire_time[r][c] = 0
            elif grid[r][c] == '&':
                cloud_r, cloud_c = r, c

    # 상하좌우 방향 벡터
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # 1. 불의 BFS 전파
    while queue:
        r, c = queue.popleft()
        
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            
            if 0 <= nr < R and 0 <= nc < C:
                # 빈 칸이거나 구름이가 있는 칸이고, 아직 불이 안 붙었다면 전파
                if grid[nr][nc] != '#' and fire_time[nr][nc] == -1:
                    fire_time[nr][nc] = fire_time[r][c] + 1
                    queue.append((nr, nc))

    # 2. 구름이 주변 및 구름이 본인 칸 중 불이 가장 먼저 도착하는 최단 시간 계산
    min_time = float('inf')
    
    # 구름이 본인 위치 확인
    if fire_time[cloud_r][cloud_c] != -1:
        min_time = min(min_time, fire_time[cloud_r][cloud_c])
        
    # 구름이 사방 인접 위치 확인
    for i in range(4):
        nr, nc = cloud_r + dr[i], cloud_c + dc[i]
        if 0 <= nr < R and 0 <= nc < C:
            if fire_time[nr][nc] != -1:
                min_time = min(min_time, fire_time[nr][nc])

    # 3. 출력 처리
    if min_time == float('inf'):
        print(-1)
    else:
        # 불이 도착하는 순간 즉시 탈출하므로 min_time초 직전까지(즉 min_time초 동안) 논문을 챙길 수 있음
        print(min_time)

if __name__ == '__main__':
    solve_fire()