import sys

def solve_goorm_rpg2():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    armor_values = [int(x) for x in data[1:N+1]]
    
    # 1. 에라토스테네스의 체로 소수 판별 배열 만들기 (최대 값 100,000)
    MAX_V = 100000
    is_prime = [True] * (MAX_V + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(MAX_V**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, MAX_V + 1, i):
                is_prime[j] = False
                
    # 2. 각 갑옷마다 가장 가까운 소수(혹은 2) 찾기
    for A in armor_values:
        current = A
        # 소수이거나 최솟값 2에 도달할 때까지 값을 1씩 내림
        while current > 2 and not is_prime[current]:
            current -= 1
            
        # 변형 횟수 = 원래 값 - 찾아낸 판타스틱 갑옷 값
        print(A - current)

if __name__ == "__main__":
    solve_goorm_rpg2()