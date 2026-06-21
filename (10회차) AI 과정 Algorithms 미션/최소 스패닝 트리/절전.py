import sys

# PyTorch나 다른 무거운 라이브러리와 충돌을 방지하기 위해 
# 재귀 깊이를 안전하게 설정합니다.
sys.setrecursionlimit(300000)
input = sys.stdin.readline


def find(x, parent):
    if parent[x] < 0:
        return x
    parent[x] = find(parent[x], parent)
    return parent[x]


def union(x, y, parent):
    root_x = find(x, parent)
    root_y = find(y, parent)

    if root_x != root_y:
        # parent[root]에는 해당 집합의 크기(음수 형태)를 저장합니다.
        parent[root_x] += parent[root_y]
        parent[root_y] = root_x
        return True
    return False


def solve():
    N, M, K = map(int, input().split())

    edges = []
    total_power = 0

    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))
        total_power += w

    # 1. 절약 전력이 작은 복도(간선)부터 오름차순 정렬
    edges.sort()

    # parent 배열 초기화 (-1은 크기가 1인 루트 노드를 의미)
    parent = [-1] * (N + 1)

    # 처음부터 K가 1이라면 이미 1번 구역 혼자서 만족하므로 
    # 아무 복도도 켤 필요 없이 모든 복도를 다 끌 수 있습니다.
    if K <= 1:
        print(total_power)
        return

    used_power = 0

    # 2. 크루스칼 알고리즘 진행
    for w, u, v in edges:
        if union(u, v, parent):
            # 1번 구역이 포함된 집합의 루트를 찾습니다.
            root_1 = find(1, parent)
            # parent[root_1]의 절대값이 곧 1번 컴포넌트의 구역(노드) 수입니다.
            current_component_size = -parent[root_1]

            # 최소 복도 전력 누적
            used_power += w

            # 1번 구역과 연결된 구역 수가 K 이상이 되는 순간 종료
            if current_component_size >= K:
                break

    # 3. 전체 전력 - 불을 켜두는데 사용한 최소 전력 = 절약할 수 있는 최대 전력
    print(total_power - used_power)


if __name__ == "__main__":
    solve()