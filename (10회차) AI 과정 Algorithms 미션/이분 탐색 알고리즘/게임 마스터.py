import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    
    # 현재 승률 (소수점 버림 정수형)
    current_Z = (M * 100) // N
    
    # 승률이 99% 이상이면 1%를 더 올리는 것은 불가능
    if current_Z >= 99:
        print("X")
        return
        
    target_Z = current_Z + 1
    answer = -1
    
    # 이진 탐색 범위 설정 (최소 1판 ~ 최대 10^12판)
    start = 1
    end = 10**12
    
    while start <= end:
        mid = (start + end) // 2
        
        # mid 판만큼 더 이겼을 때의 새로운 승률
        new_Z = ((M + mid) * 100) // (N + mid)
        
        if new_Z >= target_Z:
            answer = mid       # 우선 정답 후보로 저장하고
            end = mid - 1      # 더 적은 판수로도 가능한지 왼쪽 범위를 탐색
        else:
            start = mid + 1    # 승률이 부족하므로 더 많은 판수 필요
            
    # 문제 조건: 최소 게임 진행 횟수가 10^12회 이상이면 X 출력
    # (여기서는 추가할 판수 + 기존 판수 N이 10^12를 넘는지 체크하거나, mid 범위 자체로 판단)
    if answer == -1 or answer > 10**12:
        print("X")
    else:
        print(answer)

if __name__ == "__main__":
    solve()