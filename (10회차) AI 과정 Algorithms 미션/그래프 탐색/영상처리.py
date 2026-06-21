import sys
from collections import deque

def solve_image_processing():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    
    # 영상 픽셀 데이터 배열 생성
    grid = []
    idx = 2
    for _ in range(N):
        grid.append([int(x) for x in data[idx:idx+M]])
        idx += M
        
    # 임곗값 T
    T = int(data[idx])

    visited = [[False] * M for _ in range(N)]
    
    # 상하좌우 방향 벡터
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    
    component_count = 0
    max_component_size = 0

    # 모든 격자를 순회하며 탐색 시작
    for r in range(N):
        for c in range(M):
            # 픽셀 값이 T 이상이고 아직 방문하지 않은 칸을 만나면 새로운 객체(덩어리) 시작
            if grid[r][c] >= T and not visited[r][c]:
                component_count += 1
                
                # BFS를 통한 덩어리 크기 측정
                queue = deque([(r, c)])
                visited[r][c] = True
                current_size = 0
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_size += 1
                    
                    for i in range(4):
                        nr, nc = curr_r + dr[i], curr_c + dc[i]
                        
                        if 0 <= nr < N and 0 <= nc < M:
                            # 경계 내에 있고, 값이 T 이상이며, 방문하지 않은 경우
                            if grid[nr][nc] >= T and not visited[nr][nc]:
                                visited[nr][nc] = True
                                queue.append((nr, nc))
                
                # 최대 객체 크기 갱신
                if current_size > max_component_size:
                    max_component_size = current_size

    # 결과 출력 (객체의 개수와 가장 큰 객체의 크기)
    print(component_count)
    print(max_component_size)

if __name__ == '__main__':
    solve_image_processing()