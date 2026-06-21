import sys

def solve_staring_back():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    N = int(data[0])
    heights = [int(x) for x in data[1:N+1]]
    
    stack = []
    ans = []
    
    for h in heights:
        # 단조 감소 상태를 유지: 나보다 작거나 같은 놈들은 스택에서 제거
        # 왜냐하면 내가 더 높기 때문에 내 오른쪽에 올 신선들은 내 뒤의 작은 신선들을 볼 수 없음
        while stack and stack[-1] <= h:
            stack.pop()
            
        # 스택에 남아있는 원소의 개수가 현재 신선의 뒤통수를 볼 수 있는 신선의 수
        ans.append(len(stack))
        
        # 현재 신선 스택에 추가
        stack.append(h)
        
    print(*(ans))

if __name__ == "__main__":
    solve_staring_back()