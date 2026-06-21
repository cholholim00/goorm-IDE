import sys

def solve_weed():
    input = sys.stdin.readline
    
    N, Q = map(int, input().split())
    A = [0] + list(map(int, input().split()))
    
    tree = [0] * (N + 1)
    
    def update(idx, val):
        while idx <= N:
            tree[idx] += val
            idx += (idx & -idx)
            
    def query(idx):
        s = 0
        while idx > 0:
            s += tree[idx]
            idx -= (idx & -idx)
        return s

    # 초기 값 반영
    for i in range(1, N + 1):
        update(i, A[i])
        
    output = []
    for _ in range(Q):
        line = input().split()
        q_type = int(line[0])
        
        if q_type == 1:
            # 1 l r: l번부터 r번까지 합 출력
            l, r = int(line[1]), int(line[2])
            output.append(str(query(r) - query(l - 1)))
            
        elif q_type == 2:
            # 2 i x: i번 잡초 크기 x만큼 증가
            i, x = int(line[1]), int(line[2])
            A[i] += x
            update(i, x)
            
        elif q_type == 3:
            # 3 i x: i번 잡초 크기 x만큼 감소
            i, x = int(line[1]), int(line[2])
            A[i] -= x
            update(i, -x)
            
    print('\n'.join(output))

if __name__ == '__main__':
    solve_weed()