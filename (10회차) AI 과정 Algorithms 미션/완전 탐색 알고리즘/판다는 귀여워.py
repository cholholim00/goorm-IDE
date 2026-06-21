import sys

def solve_cute_panda():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    
    pandas = []
    panda_positions = set() # 판다가 있는 위치를 빠르게 조회하기 위한 set
    
    idx = 3
    for _ in range(K):
        r = int(data[idx])
        c = int(data[idx+1])
        pandas.append((r, c))
        panda_positions.add((r, c))
        idx += 2
        
    min_dissatisfaction = float('inf')
    
    # 모든 칸(r, c)을 돌며 판다가 없는 빈 칸 탐색 (1번부터 N번 행/열)
    for r in range(1, N + 1):
        for c in range(1, M + 1):
            # 이미 판다가 살고 있는 칸은 건너뜀
            if (r, c) in panda_positions:
                continue
            
            # 현재 칸 (r, c)에서의 불만족도 계산
            current_dissatisfaction = 0
            for pr, pc in pandas:
                current_dissatisfaction += (r - pr) ** 2 + (c - pc) ** 2
            
            # 최솟값 갱신
            if current_dissatisfaction < min_dissatisfaction:
                min_dissatisfaction = current_dissatisfaction
                
    print(min_dissatisfaction)

if __name__ == "__main__":
    solve_cute_panda()