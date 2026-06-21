import sys

def solve():
    input = sys.stdin.readline
    
    N = int(input())
    # 수열 A를 set으로 입력받아 중복 제거 및 O(1) 탐색 보장
    A_set = set(map(int, input().split()))
    
    M = int(input())
    # 질문 배열 B 입력
    B = list(map(int, input().split()))
    
    # 각 질문에 대해 존재하면 1, 없으면 0 출력
    for num in B:
        if num in A_set:
            print(1)
        else:
            print(0)

if __name__ == "__main__":
    solve()