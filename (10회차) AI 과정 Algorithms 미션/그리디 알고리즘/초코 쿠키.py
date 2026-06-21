import sys


def solve():
    # 빠른 입출력을 위해 sys.stdin.read 사용
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    # A 배열 생성 (1-indexed를 맞추기 위해 앞에 0 추가)
    A = [0] + [int(x) for x in input_data[1 : N + 1]]

    # B = [(A[i], i), ...] 쌍을 담는다.
    B = []
    for i in range(1, N + 1):
        B.append((A[i], i))

    # Ai 기준 오름차순 정렬 (값이 같으면 인덱스 i 기준 오름차순)
    B.sort()

    # 예외 처리: 쿠키를 어떤 순서로 먹어도 반드시 곱이 0이 되는 경우
    # i일(0부터 시작)이 지났을 때 쿠키의 맛있는 정도가 0 이하가 되는지 확인
    for i in range(N):
        if B[i][0] - i <= 0:
            print(*(range(1, N + 1)))
            return

    # 조건에 맞는 인덱스 순서대로 출력
    result = [idx for val, idx in B]
    print(*result)


if __name__ == "__main__":
    solve()