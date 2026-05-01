# 스택(Stack) 자료구조 구현하기

# Node 클래스: 연결 리스트의 각 노드를 나타냄
class Node:
    # 노드 초기화
    def __init__(self, data):
        self.data = data      # 노드가 저장할 데이터
        self.next = None      # 다음 노드를 가리키는 포인터 (초기값: None)

# Stack 클래스: LIFO(Last In First Out) 구조를 연결 리스트로 구현
class Stack:
    # 스택 초기화
    def __init__(self):
        self.top = None  # 스택의 맨 위(가장 최근에 추가된 노드)를 가리키는 포인터
        
    # push(data): 데이터를 스택에 추가 (O(1) 시간복잡도)
    def push(self, data):
        # 스택이 비어있는 경우
        if self.top is None:
            self.top = Node(data)  # 새 노드가 top이 됨
        else:
            # 스택에 데이터가 있는 경우
            node = Node(data)      # 새로운 노드 생성
            node.next = self.top   # 새 노드가 기존 top을 가리킴 (기존 요소 위에 쌓임)
            self.top = node        # 새 노드가 새로운 top이 됨
    
    # pop(): 스택 맨 위의 데이터를 제거하고 반환 (O(1) 시간복잡도)
    def pop(self):
        # 스택이 비어있는 경우
        if self.top is None:
            return None
        # 현재 top 노드 저장
        node = self.top
        # top을 다음 노드로 이동 (맨 위의 요소 제거)
        self.top = self.top.next
        # 제거된 노드의 데이터 반환
        return node.data
    
    # peek(): 스택 맨 위의 데이터를 확인만 함 (제거하지 않음, O(1) 시간복잡도)
    def peek(self):
        # 스택이 비어있는 경우
        if self.top is None:
            return None
        # top 노드의 데이터 반환
        return self.top.data
    
    # is_empty(): 스택이 비어있는지 확인
    def is_empty(self):
        return self.top is None  # top이 None이면 스택이 비어있음
    
if __name__ == "__main__":
    # 스택 객체 생성
    s = Stack()
        
    # 1단계: push 연산 - 스택에 데이터 추가 (A, B, C 순서로 추가)
    for i in range(3):
        s.push(chr(ord('A') + i))  # ord('A') = 65, chr(65) = 'A' 이용하여 A, B, C 생성
        print(f"Push data = {s.peek()}")  # 추가한 데이터 확인 (peek으로 제거하지 않고 확인)
    print()
    
    # 2단계: pop 연산 - 스택에서 데이터를 꺼냄 (LIFO: C, B, A 순서로 제거)
    while not s.is_empty():  # 스택이 비어있지 않은 동안 반복
        print(f"Pop data = {s.pop()}")  # 맨 위의 데이터를 제거하고 출력
    print()
        
    # 3단계: 빈 스택에서 peek 시도
    print(f"Peek data = {s.peek()}")  # 빈 스택이므로 None 출력