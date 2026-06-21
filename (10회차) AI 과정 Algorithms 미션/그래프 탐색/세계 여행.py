import sys
from collections import deque

def solve_travel():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    
    # 각 나라가 사용하는 언어 (1번 나라가 인덱스 1이 되도록 맞춤)
    languages = [0] + [int(x) for x in data[2:2+N]]
    
    # 그래프 인접 리스트 생성
    graph = [[] for _ in range(N + 1)]
    idx = 2 + N
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx+1])
        graph[u].append(v)
        graph[v].append(u)
        idx += 2

    # 구름이가 원래 아는 기본 언어 (1번 나라의 언어)
    base_lang = languages[1]
    
    max_countries = 0

    # 새로 배울 언어 X를 1부터 10까지 모두 시도 (완전 탐색)
    for X in range(1, 11):
        # 1번 나라부터 시작하는 BFS
        queue = deque([1])
        visited = [False] * (N + 1)
        visited[1] = True
        
        count = 1  # 방문한 나라 수 (1번 나라는 항상 포함)
        
        while queue:
            curr = queue.popleft()
            
            for neighbor in graph[curr]:
                if not visited[neighbor]:
                    # 다음 나라의 언어가 기본 언어이거나 새로 배운 언어 X인 경우만 이동 가능
                    if languages[neighbor] == base_lang or languages[neighbor] == X:
                        visited[neighbor] = True
                        count += 1
                        queue.append(neighbor)
                        
        # 최대 방문 가능 국가 수 갱신
        if count > max_countries:
            max_countries = count

    print(max_countries)

if __name__ == '__main__':
    solve_travel()