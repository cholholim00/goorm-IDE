import sys


def solve():
    # 빠른 입출력을 위해 sys.stdin.read 사용
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # N 입력 처리
    N = int(input_data[0])

    # 그래프 인접 리스트 초기화 (1번부터 N번 정점까지)
    G = [[] for _ in range(N + 1)]

    # 간선 정보 입력 파싱
    idx = 1
    for i in range(2, N + 1):
        Ai = int(input_data[idx])
        Li = int(input_data[idx + 1])
        idx += 2
        G[i].append((Ai, Li))
        G[Ai].append((i, Li))

    # dist 배열과 pa 배열 초기화
    dist = [0] * (N + 1)
    pa = [0] * (N + 1)

    # 비재귀적 DFS 1: 거리 계산
    def dfs1(start):
        # 스택 요소: (현재 노드, 부모 노드)
        stack = [(start, 0)]
        while stack:
            i, p = stack.pop()
            for j, k in G[i]:
                if j == p:
                    continue
                dist[j] = dist[i] + k
                stack.append((j, i))

    # 비재귀적 DFS 2: 부모 정보 계산
    def dfs2(start):
        # 스택 요소: (현재 노드, 부모 노드)
        stack = [(start, 0)]
        while stack:
            i, p = stack.pop()
            for j, k in G[i]:
                if j == p:
                    continue
                pa[j] = i
                stack.append((j, i))

    # 1. 1번 정점에서 가장 먼 정점 u 구하기
    dfs1(1)
    u = 1
    for i in range(2, N + 1):
        if dist[u] < dist[i]:
            u = i

    # 2. u번 정점에서 가장 먼 정점 v 구하기 (dist 배열 재사용을 위해 초기화)
    dist = [0] * (N + 1)
    dfs1(u)
    v = 1
    for i in range(2, N + 1):
        if dist[v] < dist[i]:
            v = i

    # 3. u를 루트로 한 트리의 정점마다 부모 구하기
    dfs2(u)

    # 4. v에서 시작해 u로 거슬러 올라가며 정답 갱신
    res = float("inf")
    i = v
    while i != 0:
        res = min(res, max(dist[i], dist[v] - dist[i]))
        i = pa[i]

    # 정답 출력
    print(res)


if __name__ == "__main__":
    solve()