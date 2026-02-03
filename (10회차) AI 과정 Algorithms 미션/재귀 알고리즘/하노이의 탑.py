import sys

# 재귀 제한 늘리기 (깊이 20이라 필수는 아니지만 안전하게)
sys.setrecursionlimit(10**6)

def solve():
    # 입력 받기
    # K: 이동 횟수
    try:
        line = sys.stdin.readline()
        if not line:
            return
        K = int(line.strip())
    except ValueError:
        return

    N = 20  # 원반 개수 고정
    
    # 기둥 상태 초기화 (1번 기둥에 20, 19, ..., 1 순서로 쌓임)
    pegs = {
        1: list(range(N, 0, -1)),
        2: [],
        3: []
    }
    
    current_move = 0 # 현재 이동 횟수

    # 하노이의 탑 재귀 함수
    def hanoi(n, start, target, aux):
        nonlocal current_move
        
        # 기저 사례
        if n == 0:
            return
        
        # 이미 K번 이동했으면 더 이상 진행하지 않음 (가지치기)
        if current_move >= K:
            return

        # 1. n-1개를 start -> aux로 이동
        hanoi(n - 1, start, aux, target)
        
        # 2. 가장 큰 원반(n)을 start -> target으로 이동 (실제 이동 수행)
        if current_move < K:
            disk = pegs[start].pop()
            pegs[target].append(disk)
            current_move += 1
            
            # K번째 이동 직후 종료
            if current_move == K:
                return

        # 3. n-1개를 aux -> target으로 이동
        hanoi(n - 1, aux, target, start)

    # 실행
    hanoi(N, 1, 3, 2)

    # 결과 출력: 각 기둥에 있는 원반들의 합
    print(sum(pegs[1]), sum(pegs[2]), sum(pegs[3]))

if __name__ == "__main__":
    solve()