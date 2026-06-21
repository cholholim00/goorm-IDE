import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    S = list(map(int, input().split()))
    
    # 오름차순 정렬
    S.sort()
    
    count = 0
    
    # 가장 큰 영향력을 가진 가수 i를 고정 (i는 최소 두 번째 인덱스 뒤부터 시작)
    for i in range(2, N):
        target = S[i]
        left = 0
        right = i - 1
        
        while left < right:
            # 두 가수의 영향력 합이 target(가장 큰 영향력) 이상이면 조건 만족!
            if S[left] + S[right] >= target:
                # S[left]가 커질수록 당연히 target 이상이 되므로, 
                # 현재 left부터 right-1까지의 모든 left 조합이 다 성립합니다.
                count += (right - left)
                # 다음 탐색을 위해 right를 한 칸 당김
                right -= 1
            else:
                # 합이 부족하므로 left를 키워서 값을 증가시킴
                left += 1
                
    print(count)

if __name__ == "__main__":
    solve()