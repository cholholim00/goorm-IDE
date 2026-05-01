print("================================================")
print("알고리즘 문제풀이: 스택(Stack) 자료구조 구현하기")
print("================================================\n")

print("1. 문자열 역순 출력 문제")
def reverse_string(s):
    return s[::-1]

# 예시
print(reverse_string("aircraft")) # 출력: "tfarcria"
print("=================================================\n")

print("2. Next Greater Element (오른쪽에서 큰 값 찾기)")
def next_greater_element(arr):
    n = len(arr)
    result = [-1] * n
    stack = []

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            index = stack.pop()
            result[index] = arr[i]
        stack.append(i)
    
    for i in range(n):
        print(f"{arr[i]} --> {result[i]}")

# 예시 1
next_greater_element([4, 5, 2, 25])
# 예시 2
next_greater_element([13, 7, 6, 12])
print("=================================================\n")

print("3. 후위 표기법 변환")
def infix_to_postfix(expr):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    stack = []
    result = ""

    for char in expr:
        if char.isdigit():
            result += char
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                result += stack.pop()
            stack.append(char)
    
    while stack:
        result += stack.pop()
    return result

print(infix_to_postfix("3+5*2")) # "352*+"