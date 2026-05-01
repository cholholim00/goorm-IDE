class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # 1. 노드 추가 (맨 뒤에 붙이기)
    def append(self, data):
        new_node = Node(data)
        if not self.head:  # 리스트가 비어있으면 헤드로 지정
            self.head = new_node
            return
        
        current = self.head
        while current.next:  # 마지막 노드까지 이동
            current = current.next
        current.next = new_node

    # 2. 노드 삭제 (특정 값을 가진 노드 제거)
    def delete(self, data):
        if not self.head:
            print("리스트가 비어있습니다.")
            return

        # 삭제할 데이터가 첫 번째 노드(Head)인 경우
        if self.head.data == data:
            self.head = self.head.next
            return

        # 중간이나 끝에서 삭제할 데이터를 찾기
        current = self.head
        prev = None
        while current and current.data != data:
            prev = current
            current = current.next

        if not current:
            print(f"데이터 {data}를 찾을 수 없습니다.")
            return

        # 이전 노드의 화살표를 다음 노드로 건너뛰게 연결
        prev.next = current.next

    # 3. 리스트 전체 출력
    def display(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        print(" -> ".join(nodes) + " -> None")

# --- 실습 수행 ---
linked_list = LinkedList()

print("1. 노드 추가:")
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.display()  # 결과: 10 -> 20 -> 30 -> None

print("\n2. 중간 노드(20) 삭제:")
linked_list.delete(20)
linked_list.display()  # 결과: 10 -> 30 -> None

print("\n3. 헤드 노드(10) 삭제:")
linked_list.delete(10)
linked_list.display()  # 결과: 30 -> None