import sys

def solve_goorm_rpg():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    # 격자판 정보 입력 받기
    grid = []
    idx = 2
    for _ in range(N):
        grid.append([int(x) for x in data[idx:idx+M]])
        idx += M
        
    # 캐릭터 초기 위치 (1-indexed를 0-indexed로 변환)
    cur_r = int(data[idx]) - 1
    cur_c = int(data[idx+1]) - 1
    
    # 이동 명령 수와 명령 문자열
    K = int(data[idx+2])
    commands = data[idx+3]
    
    # 방향 딕셔너리 정의
    dir_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    
    # 캐릭터 초기 상태
    level = 1
    exp = 0
    
    for cmd in commands:
        dr, dc = dir_map[cmd]
        nr, nc = cur_r + dr, cur_c + dc
        
        # 1. 격자판 범위를 벗어나는 경우 무시
        if not (0 <= nr < N and 0 <= nc < M):
            continue
            
        cur_r, cur_c = nr, nc
        cell_value = grid[cur_r][cur_c]
        
        # 2. 몬스터가 있는 칸인 경우 (0이 아닌 경우)
        if cell_value > 0:
            monster_level = cell_value
            
            if level >= monster_level:
                # 사냥 성공: 경험치 획득 및 몬스터 제거
                exp += monster_level
                grid[cur_r][cur_c] = 0
                
                # 레벨업 조건 확인
                if exp >= level * 10:
                    level += 1
                    exp = 0
            else:
                # 사냥 실패: 게임 종료
                print(f"DEFEAT AT LEVEL {level}")
                return
                
    # 모든 이동을 무사히 마친 경우
    print(f"VICTORY AT LEVEL {level}")

if __name__ == "__main__":
    solve_goorm_rpg()