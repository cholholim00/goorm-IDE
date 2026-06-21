import sys

def solve_inventory_cleanup():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    # 현재 재고 상태 (1번부터 N번까지의 종류를 가진 상품 배치)
    inventory = [int(x) for x in data[1:N+1]]
    
    # 문제를 단순화하기 위해 0-indexed 번호(0 ~ N-1)로 보정하여 정렬 상태와 비교
    # 올바른 상태는 오름차순으로 정렬된 상태라고 가정 (예: sorted(inventory))
    correct_target = sorted(inventory)
    
    # 각 상품이 최종적으로 가야 할 인덱스를 매핑
    # 중복이 없는 순열 형태라면 방문 여부를 체크하며 사이클을 찾음
    visited = [False] * N
    min_swaps = 0
    
    # 원본 위치와 목표 위치를 매칭하기 위해 인덱스 맵 생성
    # (실제 문제 조건에 따라 가야 할 위치 배열을 정의)
    pos_map = {val: idx for idx, val in enumerate(correct_target)}
    
    for i in range(N):
        # 이미 방문했거나, 이미 제자리에 잘 있는 경우 건너뜀
        if visited[i] or inventory[i] == correct_target[i]:
            continue
            
        # 새로운 사이클 탐색 시작
        cycle_size = 0
        curr = i
        
        while not visited[curr]:
            visited[curr] = True
            # 현재 상품이 원래 가야 하는 올바른 위치로 이동
            next_val = inventory[curr]
            curr = pos_map[next_val]
            cycle_size += 1
            
        # 크기가 K인 사이클을 해결하는 최소 횟수는 K - 1번
        if cycle_size > 0:
            min_swaps += (cycle_size - 1)
            
    print(min_swaps)

if __name__ == "__main__":
    solve_inventory_cleanup()