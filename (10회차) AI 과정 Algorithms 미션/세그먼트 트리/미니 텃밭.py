import sys

def solve_garden():
    input = sys.stdin.readline
    
    N, Q = map(int, input().split())
    # 1번 인덱스부터 사용하기 위해 앞에 0 추가
    A = [0] + list(map(int, input().split()))
    
    # 펜윅 트리(Fenwick Tree) 배열
    tree = [0] * (N + 1)
    
    # 트리에 값 추가하는 함수
    def update(idx, val):
        while idx <= N:
            tree[idx] += val
            idx += (idx & -idx)
            
    # 1부터 idx까지의 누적 합을 구하는 함수
    def query(idx):
        s = 0
        while idx > 0:
            s += tree[idx]
            idx -= (idx & -idx)
        return s

    # 초기 배열 값을 트리에 반영
    for i in range(1, N + 1):
        update(i, A[i])
        
    total_harvest = 0
    output = []
    
    for _ in range(Q):
        line = input().split()
        q_type = int(line[0])
        
        if q_type == 1:
            # 1 i x: i번 작물의 크기가 x만큼 자람
            i, x = int(line[1]), int(line[2])
            A[i] += x
            update(i, x)
            
        elif q_type == 2:
            # 2 i: i번 작물 수확 (크기는 0이 됨)
            i = int(line[1])
            current_size = A[i]
            if current_size > 0:
                total_harvest += current_size
                update(i, -current_size) # 트리의 값을 0으로 만들기 위해 차감
                A[i] = 0
                
        elif q_type == 3:
            # 3 l r: l부터 r까지의 합 구하기
            l, r = int(line[1]), int(line[2])
            range_sum = query(r) - query(l - 1)
            output.append(str(range_sum))
            
    # 3번 쿼리 결과들 출력 후 마지막에 총 수확량 출력
    if output:
        print('\n'.join(output))
    print(total_harvest)

if __name__ == '__main__':
    solve_garden()