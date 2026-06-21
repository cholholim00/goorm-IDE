import sys

def solve_battery():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    A = int(data[0])
    B = int(data[1])
    C = int(data[2])
    N = int(data[3])
    
    x_chargers = []
    y_chargers = []
    
    idx = 4
    for _ in range(N):
        price = int(data[idx])
        ctype = int(data[idx+1])
        idx += 2
        
        if ctype == 0:
            x_chargers.append(price)
        else:
            y_chargers.append(price)
            
    # 가격이 저렴한 순서대로 정렬
    x_chargers.sort()
    y_chargers.sort()
    
    total_charged = 0
    total_cost = 0
    remains = []
    
    # 1. X 타입 충전기로 A 배터리 충전
    x_for_A = min(A, len(x_chargers))
    total_charged += x_for_A
    total_cost += sum(x_chargers[:x_for_A])
    # 쓰고 남은 X 충전기는 공용 배터리(C) 후보로 돌림
    remains.extend(x_chargers[x_for_A:])
    
    # 2. Y 타입 충전기로 B 배터리 충전
    y_for_B = min(B, len(y_chargers))
    total_charged += y_for_B
    total_cost += sum(y_chargers[:y_for_B])
    # 쓰고 남은 Y 충전기도 공용 배터리(C) 후보로 돌림
    remains.extend(y_chargers[y_for_B:])
    
    # 3. 남은 충전기들을 통합 정렬하여 C 배터리 충전
    remains.sort()
    c_charged = min(C, len(remains))
    total_charged += c_charged
    total_cost += sum(remains[:c_charged])
    
    print(f"{total_charged} {total_cost}")

if __name__ == '__main__':
    solve_battery()