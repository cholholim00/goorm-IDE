import sys

def solve():
    input = sys.stdin.readline
    try:
        line = input().strip()
        if not line: return
        N = int(line)
        
        islands = []
        for i in range(N):
            # 좌표 입력 받기
            coords = list(map(int, input().split()))
            # (x좌표, y좌표, 원래인덱스) 형태로 저장
            islands.append((coords[0], coords[1], i))
            
    except ValueError:
        return

    # 1. 정렬: x좌표 오름차순 -> y좌표 오름차순
    islands.sort()

    # 결과를 담을 리스트
    results = [0] * N

    # 2. 정렬된 순서대로 약탈 가능 횟수 계산
    for rank, island in enumerate(islands):
        original_idx = island[2]
        # 내 뒤에 있는 섬의 개수 = 전체(N) - 1(나) - 내 앞의 개수(rank)
        count = N - 1 - rank
        results[original_idx] = count

    # 3. 결과 출력 (한 줄에 하나씩 아래로 출력)
    print(*results, sep='\n')

if __name__ == "__main__":
    solve()