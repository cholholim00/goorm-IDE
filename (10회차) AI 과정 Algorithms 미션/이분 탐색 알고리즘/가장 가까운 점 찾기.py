import sys
from bisect import bisect_left

def solve():
    input = sys.stdin.readline
    N, Q = map(int, input().split())
    # 점들을 입력받고 오름차순 정렬
    X = sorted(list(map(int, input().split())))
    
    for _ in range(Q):
        p = int(input())
        
        # p가 들어갈 수 있는 가장 왼쪽 인덱스 탐색
        idx = bisect_left(X, p)
        
        # 1. p가 모든 점보다 오른쪽에 있는 경우
        if idx == N:
            print(X[-1])
        # 2. p가 모든 점보다 왼쪽에 있는 경우
        elif idx == 0:
            print(X[0])
        # 3. 두 점 사이에 p가 위치하는 경우 (비교 필요)
        else:
            left_point = X[idx - 1]
            right_point = X[idx]
            
            # 거리 계산
            dist_left = p - left_point
            dist_right = right_point - p
            
            # 거리가 같으면 더 작은 좌표(왼쪽)를 출력하므로 dist_left <= dist_right
            if dist_left <= dist_right:
                print(left_point)
            else:
                print(right_point)

if __name__ == "__main__":
    solve()