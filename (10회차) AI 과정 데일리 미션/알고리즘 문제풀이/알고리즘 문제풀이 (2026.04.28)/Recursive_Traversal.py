# 전위 순회 함수 만들기 (문자열)
def perorder(tree, i=0):
    if i < len(tree):
        print(tree[i], end=" ") # 현재 노드 방문
        left = 2 * i + 1
        right = left + 1
        if left < len(tree) and tree[left] is not None:
            perorder(tree, left)  # 왼쪽 자식 노드
        if right < len(tree) and tree[right] is not None:
            perorder(tree, right) # 오른쪽 자식 노드
            
            
# 문자열 출력 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("\n전위 순회 결과(문자열): ", end="")
perorder(tree)


# 전위 순회 함수 만들기 (리스트)
def perorder(tree, i=0):
    if i < len(tree):
        res = [tree[i]] # 현재 노드 방문
        left = 2 * i + 1
        right = left + 1
        if left < len(tree) and tree[left] is not None:
            res += perorder(tree, left)  # 왼쪽 자식 노드
        if right < len(tree) and tree[right] is not None:
            res += perorder(tree, right) # 오른쪽 자식 노드
        return res
    
    
# 리스트 출력 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("\n전위 순회 결과(리스트): ", end="")
print(perorder(tree))

# 중위 순회 함수 만들기
def inorder(tree):
    def _inorder(i=0):
        if i >= len(tree) or tree[i] is None:
            return 
        _inorder(2 * i + 1) # 왼쪽 자식 노드
        res.append(tree[i]) # 현재 노드 방문
        _inorder(2 * i + 2) # 오른쪽 자식 노드
        
    res = []
    _inorder()
    return res

# 중위 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("중위 순회 결과: ", end="")
print(inorder(tree))

# 후위 순회 함수 만들기
def postorder(tree):
    def _postorder(i=0):
        if i >= len(tree) or tree[i] is None:
            return 
        _postorder(2 * i + 1) # 왼쪽 자식 노드
        _postorder(2 * i + 2) # 오른쪽 자식 노드
        res.append(tree[i]) # 현재 노드 방문
        
    res = []
    _postorder()
    return res

# 후위 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("후위 순회 결과: ", end="")
print(postorder(tree))

print("===============================================================")

# 스택을 이용한 전위 순회 함수 만들기
def perorder(tree):
    if not tree:
        return []
    
    res, stack = [],[0] # 루트 노드 인덱스부터 시작
    
    while stack:
        parent = stack.pop()
        res.append(tree[parent]) # 현재 노드 방문
        left = 2 * parent + 1
        right = left + 1
        if right < len(tree) and tree[right] is not None:
            stack.append(right) # 오른쪽 자식 노드 먼저 스택에 추가 (나중에 방문)
        if left < len(tree) and tree[left] is not None:
            stack.append(left) # 왼쪽 자식 노드 먼저 스택에 추가 (후에 방문)
    return res

# 스택을 이용한 전위 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("전위 순회 결과(스택): ", end="")
print(perorder(tree))

# 스택을 이용한 중위 순회 함수 만들기
def inorder(tree):
    if not tree:
        return []
    
    index = 0 # 현재 노드 인덱스
    res, stack = [],[]
    
    while True:
        if index < len(tree) and tree[index] is not None:
            stack.append(index) # 현재 노드 인덱스 스택에 추가
            index = 2 * index + 1 # 왼쪽 자식 노드로 이동
        elif stack:
            index = stack.pop()
            res.append(tree[index]) # 현재 노드 방문
            index = 2 * index + 2 # 오른쪽 자식 노드로 이동
        else:
            break
    return res

# 스택을 이용한 중위 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("중위 순회 결과(스택): ", end="")
print(inorder(tree))

# 스택을 이용한 후위 순회 함수 만들기
def postorder(tree):
    if not tree:
        return []
    
    res, stack = [],[0] # 루트 노드 인덱스부터 시작
    visit_order = [] # 방문 순서 기록
    
    while stack:
        index = stack.pop()
        visit_order.append(index) # 방문 순서 기록
        index = 2 * index + 1
        if index < len(tree) and tree[index] is not None:
            stack.append(index) # 왼쪽 자식 노드 먼저 스택에 추가 (나중에 방문)
        index = index + 1
        if index < len(tree) and tree[index] is not None:
            stack.append(index) # 오른쪽 자식 노드 먼저 스택에 추가 (후에 방문)
            
    while visit_order:
        index = visit_order.pop()
        res.append(tree[index]) # 방문 순서 역순으로 결과에 추가
    return res

# 스택을 이용한 후위 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("후위 순회 결과(스택): ", end="")
print(postorder(tree))

print("===============================================================")
# 큐를 이용한 레벨 순회 함수 만들기

def levelorder(tree):
    if not tree:
        return []
    
    res, queue = [], [0] # 루트 노드 인덱스부터 시작
    
    while queue:
        index = queue.pop(0)
        res.append(tree[index]) # 현재 노드 방문
        index = 2 * index + 1
        if index < len(tree) and tree[index] is not None:
            queue.append(index) # 왼쪽 자식 노드 큐에 추가
        index += 1
        if index < len(tree) and tree[index] is not None:
            queue.append(index) # 오른쪽 자식 노드 큐에 추가
    return res

# 큐를 이용한 레벨 순회 결과 test
tree = ["A", "B", "C", "D", "E", "F", None,"G"]
print("레벨 순회 결과(큐): ", end="")
print(levelorder(tree))

print("===============================================================")

# 연결 리스트로 이진트리 표현하기 - 재귀 순회 함수 만들기
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        
class Tree:
    def __init__(self):
        self.root = None
        
    # 연결 리스트로 표현된 이진트리의 전위, 중위, 후위 순회 함수 만들기
    def perorder(self):
        def _perorder(node):
            if node is None:
                return
            res.append(node.data) # 현재 노드 방문
            _perorder(node.left) # 왼쪽 자식 노드
            _perorder(node.right) # 오른쪽 자식 노드

        res = []
        _perorder(self.root)
        return res

    def inorder(self):
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left) # 왼쪽 자식 노드
            res.append(node.data) # 현재 노드 방문
            _inorder(node.right) # 오른쪽 자식 노드

        res = []
        _inorder(self.root)
        return res

    def postorder(self):
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left) # 왼쪽 자식 노드
            _postorder(node.right) # 오른쪽 자식 노드
            res.append(node.data) # 현재 노드 방문

        res = []
        _postorder(self.root)
        return res

if __name__ == "__main__":
    tree = Tree()
    tree.root = Node("A")
    tree.root.left = Node("B")
    tree.root.right = Node("C")
    tree.root.left.left = Node("D")
    tree.root.left.right = Node("E")
    tree.root.right.left = Node("F")
    tree.root.left.left.left = Node("G")
    
# 연결 리스트로 표현된 이진트리의 전위, 중위, 후위 순회 결과 출력
print("전위 순회 결과(연결 리스트): ", end="")
print(tree.perorder())
print("중위 순회 결과(연결 리스트): ", end="")
print(tree.inorder())
print("후위 순회 결과(연결 리스트): ", end="")
print(tree.postorder())

print("===============================================================")
# 연결 리스트로 이진트리 표현하기 - 레벨 순서 순회 함수 만들기
class Tree:
    ...
    
    def levelorder(self):
        res = [] # 레벨 순회 결과를 저장할 리스트
        if not self.root:
            return res

        queue = [self.root] # 루트 노드부터 시작
        while queue:
            node = queue.pop(0)
            res.append(node.data) # 현재 노드 방문
            if node.left:
                queue.append(node.left) # 왼쪽 자식 노드 큐에 추가
            if node.right:
                queue.append(node.right) # 오른쪽 자식 노드 큐에 추가
        return res
    
if __name__ == "__main__":
    tree = Tree()
    tree.root = Node("A")
    tree.root.left = Node("B")
    tree.root.right = Node("C")
    tree.root.left.left = Node("D")
    tree.root.left.right = Node("E")
    tree.root.right.left = Node("F")
    tree.root.left.left.left = Node("G")
    
# 연결 리스트로 표현된 이진트리의 레벨 순회 결과 출력
print("레벨 순회 결과(연결 리스트): ", end="")
print(tree.levelorder())

print("===============================================================")
# 이진트리 클래스의 전체코드 구성하기
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        
class Tree:
    def __init__(self):
        self.root = None
        
    def perorder(self):
        def _perorder(node):
            if node is None:
                return
            res.append(node.data) # 현재 노드 방문
            _perorder(node.left) # 왼쪽 자식 노드
            _perorder(node.right) # 오른쪽 자식 노드

        res = []
        _perorder(self.root)
        return res
    
    def inorder(self):
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left) # 왼쪽 자식 노드
            res.append(node.data) # 현재 노드 방문
            _inorder(node.right) # 오른쪽 자식 노드

        res = []
        _inorder(self.root)
        return res
    
    def postorder(self):
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left) # 왼쪽 자식 노드
            _postorder(node.right) # 오른쪽 자식 노드
            res.append(node.data) # 현재 노드 방문

        res = []
        _postorder(self.root)
        return res
    def levelorder(self):
        res = [] # 레벨 순회 결과를 저장할 리스트
        if not self.root:
            return res

        queue = [self.root] # 루트 노드부터 시작
        while queue:
            node = queue.pop(0)
            res.append(node.data) # 현재 노드 방문
            if node.left:
                queue.append(node.left) # 왼쪽 자식 노드 큐에 추가
            if node.right:
                queue.append(node.right) # 오른쪽 자식 노드 큐에 추가
        return res
    
    def make_tree(self, arr):
        if not arr:
            return
        self.root = Node(arr[0]) # 루트 노드 생성
        q = [self.root] # 노드 생성에 사용할 큐
        index = 1
        
        while q and index < len(arr):
            node = q.pop(0)
            if index < len(arr) and arr[index] is not None:
                node.left = Node(arr[index]) # 왼쪽 자식 노드 생성
                q.append(node.left) # 왼쪽 자식 노드 큐에 추가
            index += 1
            if index < len(arr) and arr[index] is not None:
                node.right = Node(arr[index]) # 오른쪽 자식 노드 생성
                q.append(node.right) # 오른쪽 자식 노드 큐에 추가
            index += 1
            
if __name__ == "__main__":
    tree = Tree()
    tree.make_tree(["A", "B", "C", "D", "E", "F", None, "G"])

# 배열로 표현된 이진트리를 연결 리스트로 변환한 후, 전위 순회와 레벨 순회 결과 출력
print("전위 순회 결과(연결 리스트 변환): ", end="")
print(tree.perorder())
print("레벨 순회 결과(연결 리스트 변환): ", end="")
print(tree.levelorder())