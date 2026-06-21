import sys

def solve():
    # 빠른 입출력 설정
    input = sys.stdin.readline
    
    # N: 놀이기구 개수
    N = int(input())
    
    # F: 재미도 배열 (1번 인덱스부터 맞추기 위해 앞에 [0] 추가)
    F = [0] + list(map(int, input().split()))
    
    # Q: 날의 수(쿼리 개수)
    Q = int(input())
    
    # 누적 합 배열 P 초기화
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = P[i - 1] + F[i]
        
    # 쿼리 처리
    output = []
    for _ in range(Q):
        L, R = map(int, input().split())
        # 구간 합 공식: P[R] - P[L - 1]
        day_sum = P[R] - P[L - 1]
        output.append(str(day_sum))
        
    # 결과 일괄 출력
    print('\n'.join(output))

if __name__ == '__main__':
    solve()