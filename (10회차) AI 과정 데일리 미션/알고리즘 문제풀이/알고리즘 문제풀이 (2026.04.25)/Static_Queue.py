# 큐(Queue) 자료구조 구현하기
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
class Queue:
    def __init__(self):
        self.front = None  # 큐의 맨 앞을 가리키는 포인터
        self.rear = None   # 큐의 맨 뒤를 가리키는 포인터
        
    def enqueue(self, data):
        if self.rear is None:  # 큐가 비어있는 경우
            self.front = self.rear = Node(data)  # 새 노드가 front와 rear이 됨
        else:
            node = Node(data)                # 새로운 노드 생성
            self.rear.next = node  # 기존 rear의 다음 노드로 새 노드 연결
            self.rear = node       # 새 노드가 새로운 rear이 됨
            
    def dequeue(self):
        if self.front is None:  # 큐가 비어있는 경우
            return None
        node = self.front      # 현재 front 노드 저장
        if self.front == self.rear:  # 큐에 요소가 하나만 있는 경우, front와 rear 모두 None으로 설정
            self.front = self.rear = None
        else:
            self.front = self.front.next  # front를 다음 노드로 이동 (맨 앞의 요소 제거)
        return node.data       # 제거된 노드의 데이터 반환
    
    def is_empty(self):
        return self.front is None  # front이 None이면 큐가 비어있음
    
if __name__ == "__main__":
    q = Queue()
    
    # 1단계: enqueue 연산 - 큐에 데이터 추가 (A, B, C 순서로 추가)
    for i in range(3):
        q.enqueue(chr(ord('A') + i))  # ord('A') = 65, chr(65) = 'A' 이용하여 A, B, C 생성
        print(f"Enqueue data = {q.rear.data}")  # 추가한 데이터 확인
    print()
    
    # 2단계: dequeue 연산 - 큐에서 데이터 제거 및 반환 (FIFO 순서로 제거)
    while not q.is_empty():
        print(f"Dequeue data = {q.dequeue()}")  # 제거된 데이터 확인