import sys

def solve_goorm_flag():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    K = int(data[1])  # 찾고자 하는 깃발의 값
    
    # 격자판 정보 입력 받기
    grid = []
    idx = 2
    for _ in range(N):
        grid.append([int(x) for x in data[idx:idx+N]])
        idx += N
        
    # 주변 8방향 설정을 위한 상대 좌표 (상, 하, 좌, 우, 대각선 4방향)
    dr = [-1, -1, -1, 0, 0, 1, 1, 1]
    dc = [-1, 0, 1, -1, 1, -1, 0, 1]
    
    target_flag_count = 0
    
    # 격자의 모든 칸을 순회
    for r in range(N):
        for c in range(N):
            # 구름이 이미 있는 칸('1')은 깃발을 꽂을 수 없으므로 건너뜀
            if grid[r][c] == 1:
                continue
                
            # 주변 8칸의 구름 개수 세기
            cloud_count = 0
            for i in range(8):
                nr, nc = r + dr[i], c + dc[i]
                
                # 격자 범위를 만족하고 그 칸이 구름('1')인 경우 카운트 증가
                if 0 <= nr < N and 0 <= nc < N:
                    if grid[nr][nc] == 1:
                        cloud_count += 1
                        
            # 세어진 구름의 개수가 목표값 K와 일치하면 카운트
            if cloud_count == K:
                target_flag_count += 1
                
    print(target_flag_count)

if __name__ == "__main__":
    solve_goorm_flag()