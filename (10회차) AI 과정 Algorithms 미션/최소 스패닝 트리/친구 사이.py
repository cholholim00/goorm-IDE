import sys

sys.setrecursionlimit(300000)
input = sys.stdin.readline


def find(x, parent):
    if parent[x] == x:
        return x
    parent[x] = find(parent[x], parent)
    return parent[x]


def union(x, y, parent):
    root_x = find(x, parent)
    root_y = find(y, parent)

    if root_x != root_y:
        parent[root_y] = root_x
        return True
    return False


def solve():
    N = int(input())
    M = int(input())

    parent = list(range(N + 1))
    required_edges = N - 1
    connected_count = 0

    # 1. 이미 친분이 있는 M개의 쌍을 먼저 유니온 처리
    for _ in range(M):
        u, v = map(int, input().split())
        if union(u, v, parent):
            connected_count += 1

    K = int(input())
    new_edges = []

    for _ in range(K):
        u, v, w = map(int, input().split())
        new_edges.append((w, u, v))

    # 2. 새로 친분을 쌓을 수 있는 쌍을 시간(비용) 기준으로 오름차순 정렬
    new_edges.sort()

    total_time = 0

    # 3. 크루스칼 알고리즘으로 나머지 컴포넌트들을 연결
    for w, u, v in new_edges:
        # 이미 모두가 연결되었다면 조기 종료
        if connected_count == required_edges:
            break

        if union(u, v, parent):
            total_time += w
            connected_count += 1

    # 4. 모든 컴포넌트가 하나로 합쳐졌는지 확인 (간선 개수가 N-1개인지)
    if connected_count == required_edges:
        print(total_time)
    else:
        print(-1)


if __name__ == "__main__":
    solve()