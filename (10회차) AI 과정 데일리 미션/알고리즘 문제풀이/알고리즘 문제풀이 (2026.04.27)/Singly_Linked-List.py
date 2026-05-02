## 1. Node 클래스 정의
# 먼저 링크드리스트의 삽입,삭제,출력,탐색을 구현
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
## 2. SinglyLinkedList 클래스 정의
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # 1. 삽입 (Insertion) - 리스트 끝에 추가
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # 2. 삭제 (Deletion) - 특정 값을 가진 노드 삭제
    def delete(self, key):
        current = self.head
        
        # 삭제할 노드가 head인 경우
        if current and current.data == key:
            self.head = current.next
            current = None
            return

        # 삭제할 노드 탐색
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        # 값이 리스트에 없는 경우
        if not current:
            print(f"값 {key}를 찾을 수 없습니다.")
            return

        # 연결 끊기
        prev.next = current.next
        current = None

    # 3. 탐색 (Search) - 특정 값이 있는지 확인
    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    # 4. 출력 (Display) - 전체 리스트 보기
    def display(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        print(" -> ".join(nodes) + " -> None")

# 사용 예시
sll = SinglyLinkedList()
sll.append(10)
sll.append(20)
sll.append(30)
sll.display()          # 10 -> 20 -> 30 -> None

print(sll.search(20))  # True
sll.delete(20)
sll.display()          # 10 -> 30 -> None