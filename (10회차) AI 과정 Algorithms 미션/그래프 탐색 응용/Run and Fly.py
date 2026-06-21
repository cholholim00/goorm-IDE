import sys
from collections import deque

def solve_run_and_fly():
    input = sys.stdin.readline
    N, M, T = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    
    # 상하좌우 이동 방향
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    # 주어진 K 값으로 T초 이내에 도달 가능한지 체크하는 BFS
    def can_escape(K):
        # visited[r][c][energy] = 현재 칸에 특정 에너지로 도달했을 때의 최소 시간
        # 시간 제한 T가 최대 1000이므로 3차원 배열 대신 딕셔너리나 최적화된 배열을 쓸 수 있습니다.
        # 여기서는 메모리와 속도를 위해 큐에 (r, c, energy, time)을 넣고 방문 체크를 (r, c, energy)로 관리합니다.
        
        visited = [[[False] * (K + 1) for _ in range(M)] for _ in range(N)]
        queue = deque([(0, 0, K, 0)])  # r, c, current_energy, time
        visited[0][0][K] = True
        
        while queue:
            r, c, e, t = queue.popleft()
            
            if r == N - 1 and c == M - 1:
                return True
                
            if t >= T:
                continue
                
            # 1. 상하좌우 이동
            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] != 0:
                    next_type = grid[nr][nc]
                    curr_type = grid[r][c]
                    
                    # 이동 시 에너지 소모 판정
                    # 땅(2) -> 땅(2) 외에는 모두 에너지를 1 소모함
                    if curr_type == 2 and next_type == 2:
                        next_e = e
                    else:
                        next_e = e - 1
                        
                    if next_e >= 0 and not visited[nr][nc][next_e]:
                        visited[nr][nc][next_e] = True
                        queue.append((nr, nc, next_e, t + 1))
            
            # 2. 제자리 휴식 (현재 땅(2)이고 에너지가 K 미만일 때만 가능)
            if grid[r][c] == 2 and e < K:
                next_e = e + 1
                if not visited[r][c][next_e]:
                    visited[r][c][next_e] = True
                    queue.append((r, c, next_e, t + 1))
                    
        return False

    # K에 대한 이분 탐색 (범위: 0 ~ T)
    low, high = 0, T
    ans = -1
    
    while low <= high:
        mid = (low + high) // 2
        if can_escape(mid):
            ans = mid
            high = mid - 1  # 최솟값을 찾기 위해 범위를 좁힘
        else:
            low = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve_run_and_fly()