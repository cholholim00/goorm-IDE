def hanoi(n, start, target, aux):
    # 기본 케이스: 원판이 1개일 때는 바로 옮기면 끝
    if n == 1:
        print(f"원판 1을 {start}에서 {target}으로 이동")
        return

    # 1단계: n-1개를 보조 기둥으로 이동 (목표 기둥을 보조로 활용)
    hanoi(n - 1, start, aux, target)

    # 2단계: 가장 큰 원판을 목표 기둥으로 이동
    print(f"원판 {n}을 {start}에서 {target}으로 이동")

    # 3단계: 보조 기둥에 있던 n-1개를 목표 기둥으로 이동 (시작 기둥을 보조로 활용)
    hanoi(n - 1, aux, target, start)

# 실행 예시: 원판 3개를 A에서 C로 이동 (B는 보조)
print("--- 하노이의 탑 이동 순서 ---")
hanoi(3, 'A', 'C', 'B')