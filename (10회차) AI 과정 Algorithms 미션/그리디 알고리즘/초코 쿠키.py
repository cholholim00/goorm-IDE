import sys

def solve_cookie():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    N = int(data[0])
    cookies = []
    
    # 쿠키 번호는 1번부터 N번까지 순서대로 부여됨
    for i in range(N):
        A = int(data[i+1])
        cookies.append((A, i + 1))
        
    # 기본 정렬: 맛(A) 내림차순, 맛이 같다면 원래 번호(인덱스) 오름차순
    cookies.sort(key=lambda x: (-x[0], x[1]))
    
    result = []
    zero_idx = -1
    
    # 시뮬레이션을 돌려 맛이 0 이하가 되는 순간(곱이 0이 되는 지점)을 찾음
    for j in range(N):
        current_taste = cookies[j][0] - j
        if current_taste <= 0:
            zero_idx = j
            break
        result.append(cookies[j][1])
        
    # 만약 곱이 0이 되는 지점이 존재한다면
    if zero_idx != -1:
        # 이 시점부터 남은 쿠키들은 맛의 곱에 영향을 주지 않으므로 (전체 곱이 0)
        # 사전순으로 가장 앞서기 위해 '원래 번호(인덱스)' 기준으로 정렬
        remaining_cookies = cookies[zero_idx:]
        remaining_cookies.sort(key=lambda x: x[1])
        
        for cookie in remaining_cookies:
            result.append(cookie[1])
            
    print(*(result))

if __name__ == '__main__':
    solve_cookie()