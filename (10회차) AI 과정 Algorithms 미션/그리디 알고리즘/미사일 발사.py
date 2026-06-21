import sys

def solve_missile():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    
    total_original_time = 0
    events = {}
    
    idx = 1
    for _ in range(N):
        X = int(data[idx])
        Y = int(data[idx+1])
        T = int(data[idx+2])
        idx += 3
        
        # 유클리드 거리의 제곱 d^2
        d_sq = X*X + Y*Y
        original_flight = 2 * d_sq
        total_original_time += original_flight
        
        if original_flight == 0:
            continue
            
        # 부스터 시작 짝수 시각 t의 범위: [T, T + original_flight - 2]
        start = T
        end = T + original_flight - 2
        
        # 스위핑을 위한 이벤트 등록 (+1, -1)
        # end 다음 짝수 시각인 end + 2에서 이득이 끝나므로 마킹
        events[start] = events.get(start, 0) + 1
        events[end + 2] = events.get(end + 2, 0) - 1

    # 시각 순서대로 정렬하여 스위핑
    sorted_times = sorted(events.keys())
    
    max_benefit = 0
    current_benefit = 0
    
    for t in sorted_times:
        current_benefit += events[t]
        if current_benefit > max_benefit:
            max_benefit = current_benefit
            
    # 최소 전체 시간 출력
    print(total_original_time - max_benefit)

if __name__ == '__main__':
    solve_missile()