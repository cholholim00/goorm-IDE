import sys

def solve():
    input = sys.stdin.readline
    
    # 첫째 줄 입력: N, K
    try:
        line1 = input().split()
        if not line1: return
        N, K = map(int, line1)
        
        # 둘째 줄 입력: 수열 A
        line2 = input().split()
        nums = list(map(int, line2))
    except ValueError:
        return

    # 정렬 기준 설정
    # 1순위: 1의 개수 내림차순 (-bin(x).count('1'))
    # 2순위: 숫자 크기 내림차순 (-x)
    # 튜플 형태로 키를 주면 순서대로 우선순위가 적용됩니다.
    nums.sort(key=lambda x: (-bin(x).count('1'), -x))

    # K번째 위치한 수 출력 (인덱스는 K-1)
    print(nums[K-1])

if __name__ == "__main__":
    solve()