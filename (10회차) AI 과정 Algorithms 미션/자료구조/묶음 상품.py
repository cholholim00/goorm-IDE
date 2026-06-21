import sys
# 재귀 깊이 제한 해제 (Union-Find의 find 연산 대비)
sys.setrecursionlimit(200000)

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x]) # 경로 압축 (Path Compression)
    return parent[x]

def union(parent, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    
    if root_x != root_y:
        parent[root_y] = root_x
        return True # 실제로 두 그룹이 합쳐짐
    return False # 이미 같은 그룹임

def solve_bundle_products():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    # 부모 테이블 초기화 (자기 자신을 부모로 설정)
    parent = list(range(N + 1))
    
    # 최초 그룹의 개수는 N개
    group_count = N
    
    idx = 2
    for _ in range(M):
        a = int(data[idx])
        b = int(data[idx+1])
        idx += 2
        
        # 두 물건의 그룹을 합치기 시도
        if union(parent, a, b):
            # 성공적으로 합쳐졌다면 독립된 그룹이 하나 줄어듬
            group_count -= 1
            
    print(group_count)

if __name__ == "__main__":
    solve_bundle_products()