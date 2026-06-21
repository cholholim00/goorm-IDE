import sys

def solve_bomb_defusal():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    
    # 각 기폭 장치의 전선 연결 개수(차수) 기록
    degree = [0] * (N + 1)
    # 전선 리스트 저장 (1번부터 M번까지 순서대로)
    wires = []
    
    idx = 2
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx+1])
        wires.append((u, v))
        degree[u] += 1
        degree[v] += 1
        idx += 2
        
    safe_wires = []
    
    # 1번 전선부터 하나씩 검사
    for i, (u, v) in enumerate(wires, start=1):
        # 해당 전선을 끊었을 때, u와 v 장치 모두에 다른 전선이 최소 1개 이상 남아있어야 함
        # 즉, 끊기 전 차수가 둘 다 2 이상이어야 안전합니다.
        if degree[u] >= 2 and degree[v] >= 2:
            safe_wires.append(str(i))
            
    if safe_wires:
        print(' '.join(safe_wires))
    else:
        print("-1")

if __name__ == '__main__':
    solve_bomb_defusal()