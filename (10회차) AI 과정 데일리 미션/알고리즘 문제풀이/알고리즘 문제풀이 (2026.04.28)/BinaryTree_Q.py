from collections import deque

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# 1. 이진 트리에 키 삽입하기 (레벨 순서)
def insert(root, key):
    if not root:
        return Node(key)
    
    queue = deque([root])
    while queue:
        temp = queue.popleft()
        if not temp.left:
            temp.left = Node(key)
            break
        else:
            queue.append(temp.left)
            
        if not temp.right:
            temp.right = Node(key)
            break
        else:
            queue.append(temp.right)
    return root

# 2. 가장 깊은 노드 삭제 보조 함수
def delete_deepest(root, d_node):
    queue = deque([root])
    while queue:
        temp = queue.popleft()
        if temp is d_node:
            temp = None
            return
        if temp.right:
            if temp.right is d_node:
                temp.right = None
                return
            queue.append(temp.right)
        if temp.left:
            if temp.left is d_node:
                temp.left = None
                return
            queue.append(temp.left)

# 3. 이진 트리에서 키 삭제하기
def deletion(root, key):
    if not root:
        return None
    if not root.left and not root.right:
        return None if root.key == key else root

    key_node = None
    temp = None
    queue = deque([root])
    
    # [수정] 모든 노드를 탐색하여 삭제할 노드와 가장 깊은 노드(temp)를 찾음
    while queue:
        temp = queue.popleft()
        if temp.key == key:
            key_node = temp
        if temp.left:
            queue.append(temp.left)
        if temp.right:
            queue.append(temp.right)

    
    if key_node:
        last_val = temp.key
        delete_deepest(root, temp)
        key_node.key = last_val
    return root

# 4. 결과 확인을 위한 순회 함수 
def inorder(temp):
    if not temp:
        return
    inorder(temp.left)
    print(temp.key, end=" ")
    inorder(temp.right)

if __name__ == "__main__":
    root = Node(13)
    root = insert(root, 12)
    root = insert(root, 10)
    root = insert(root, 4)
    root = insert(root, 19)
    root = insert(root, 16)
    root = insert(root, 9)

    print("삭제 전 :", end=" ")
    inorder(root) # 예상: 4 12 19 13 16 10 9
    
    print("\n노드 12 삭제 수행...")
    root = deletion(root, 12)
    
    print("삭제 후 :", end=" ")
    inorder(root) # 예상: 4 9 19 13 16 10