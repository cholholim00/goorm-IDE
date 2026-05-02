## 1. Node 클래스 정의
# 이전 노드를 가리키는 prev 변수가 추가됩니다.
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        
## 2. DoublyLinkedList 클래스 정의
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None  # 끝에서도 바로 접근할 수 있도록 tail 추가

    # 1. 삽입 (Insertion) - 리스트 끝에 추가
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
            return
        
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    # 2. 삭제 (Deletion) - 특정 값을 가진 노드 삭제
    def delete(self, key):
        current = self.head
        
        while current:
            if current.data == key:
                # 1) 삭제할 노드가 head인 경우
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                    else: # 리스트에 노드가 하나뿐이었을 경우
                        self.tail = None
                
                # 2) 삭제할 노드가 tail인 경우
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None
                
                # 3) 중간 노드인 경우
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                
                return True # 삭제 성공
            current = current.next
        return False # 삭제 실패

    # 3. 탐색 (Search) - 정방향 탐색
    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    # 4. 출력 (Display) - 정방향 출력
    def display(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        print(" <-> ".join(nodes) + " <-> None")

# 사용 예시
dll = DoublyLinkedList()
dll.append(100)
dll.append(200)
dll.append(300)
dll.display()           # 100 <-> 200 <-> 300 <-> None

dll.delete(200)
dll.display()           # 100 <-> 300 <-> None
print(dll.search(300))  # True