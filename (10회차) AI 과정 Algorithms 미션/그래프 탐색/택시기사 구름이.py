from collections import deque
import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    def rd():
        nonlocal idx
        v = data[idx]; idx += 1
        return int(v)
    
    N, M = rd(), rd()
    X, Y, Z = rd(), rd(), rd()
    S = 5  # 문제에서 고정: 거리 5 이하면 기본요금 X
    
    # grid[row][col] (0-indexed)
    grid = []
    for i in range(N):
        row = [rd() for _ in range(N)]
        grid.append(row)
    
    # (a, b) = (열, 행), 1-indexed → grid[b-1][a-1]
    passengers = []
    for _ in range(M):
        a, b, c, d = rd(), rd(), rd(), rd()
        # 승차: col=a, row=b / 하차: col=c, row=d
        passengers.append((a, b, c, d))
    
    def bfs(sc, sr, ec, er):
        """(col,row) 좌표 기준 BFS. 승하차 지점은 grid=1이어도 허용."""
        if sr == er and sc == ec:
            return 0
        vis = [[-1]*N for _ in range(N)]
        q = deque([(sr-1, sc-1, 0)])
        vis[sr-1][sc-1] = 0
        while q:
            r, c, dist = q.popleft()
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < N and 0 <= nc < N and vis[nr][nc] == -1:
                    if grid[nr][nc] == 0 or (nr == er-1 and nc == ec-1):
                        vis[nr][nc] = dist+1
                        if nr == er-1 and nc == ec-1:
                            return dist+1
                        q.append((nr, nc, dist+1))
        return -1
    
    def fare(dist):
        if dist <= S:
            return X
        else:
            return X + (dist - S) * Y
    
    total_earned = 0
    total_toll = 0
    
    # 택시 초기 위치 = 첫 번째 손님 승차 지점
    cur_c, cur_r = passengers[0][0], passengers[0][1]
    
    for ac, ar, dc, dr in passengers:
        # 현재 위치 → 승차 지점
        d_pickup = bfs(cur_c, cur_r, ac, ar)
        # 승차 → 하차
        d_drop = bfs(ac, ar, dc, dr)
        
        earned = fare(d_drop)
        toll = (d_pickup + d_drop) * Z
        
        total_earned += earned
        total_toll += toll
        
        cur_c, cur_r = dc, dr
    
    print(total_earned - total_toll)

main()