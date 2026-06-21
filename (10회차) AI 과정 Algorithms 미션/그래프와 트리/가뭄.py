import sys

def solve_drought():
    # 빠른 입출력을 위해 sys.stdin.read 사용
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    T = int(input_data[0])
    idx = 1
    
    out = []
    for _ in range(T):
        N = int(input_data[idx])
        M = int(input_data[idx+1])
        idx += 2
        
        # M개의 간선 정보는 정답에 영향을 주지 않으므로 건너뜁니다.
        idx += 2 * M
        
        # 항상 모든 지점이 연결되려면 N-1개의 수로가 필요합니다.
        out.append(str(N - 1))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve_drought()