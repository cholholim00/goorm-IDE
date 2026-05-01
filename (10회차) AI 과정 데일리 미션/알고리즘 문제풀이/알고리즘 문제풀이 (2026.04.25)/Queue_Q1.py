print("================================================")
print("알고리즘 문제풀이: 큐(Queue) 자료구조 구현하기")
print("================================================\n")

from collections import deque

print("1. 요세푸스 순열 문제")
def josephus(n, k):
    queue = deque(range(1, n + 1))
    result = []
    
    while queue:
        for _ in range(k - 1):
            queue.append(queue.popleft())
        result.append(queue.popleft())
        
    return result

print(josephus(7, 3)) # [3, 6, 2, 7, 5, 1, 4]

print("=================================================\n")
print("2. 1부터 n까지의 이진수 출력 문제")
from collections import deque

def generate_binary(n):
    queue = deque(["1"])
    for _ in range(n):
        current = queue.popleft()
        print(current, end=" ")
        queue.append(current + "0")
        queue.append(current + "1")

# n=5일 때 예시
generate_binary(5) # 1 10 11 100 101