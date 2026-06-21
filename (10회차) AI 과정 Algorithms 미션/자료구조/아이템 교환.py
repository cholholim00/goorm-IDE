import sys

def solve_item_exchange():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    # 예시 구조: N개의 등급이 있고 등급별 교환 비율과 현재 보유량이 주어지는 경우
    N = int(data[0])
    
    # 등급 간 필요 개수 (i번째 아이템을 i+1번째로 바꾸는데 필요한 개수)
    # N-1 등급까지의 변환 비율이 주어짐
    req_counts = [int(x) for x in data[1:N]]
    
    # 현재 내가 가지고 있는 각 등급별 아이템 수 (1등급부터 N등급까지)
    current_items = [int(x) for x in data[N:]]
    
    # 낮은 등급(0번 인덱스)부터 순차적으로 상위 등급으로 교환 진행
    for i in range(N - 1):
        # 현재 등급에서 상위 등급으로 바꿀 수 있는 개수 계산
        exchangeable = current_items[i] // req_counts[i]
        
        # 상위 등급 아이템 개수 추가
        current_items[i+1] += exchangeable
        # 교환 후 남은 아이템 갱신
        current_items[i] %= req_counts[i]
        
    # 최종적으로 가장 높은 등급(N등급)의 아이템 개수 출력
    print(current_items[-1])

if __name__ == "__main__":
    solve_item_exchange()