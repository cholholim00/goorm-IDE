# 자식 노드 찾기
tree = ["A", "B", "C", "D", "E", "F", None, "G"]
print("\n=== 자식 노드 찾기 ===")
i = 0
n = len(tree)
while i < n:
    if tree[i]:
        print(f"부모 노드: {tree[i]}", end=", ")
        left = 2 * i + 1
        right = left + 1
        if left < n and tree[left] is not None:
            print(f"왼쪽 자식: {tree[left]}", end=", ")
        if right < n and tree[right] is not None:
            print(f"오른쪽 자식: {tree[right]}", end=" ")
        print()
    i += 1
    
# 부모 노드 찾기

print("\n=== 부모 노드 찾기 ===")
i = n - 1
while i > 0:
    if tree[i]:
        print(f"부모 노드 찾기: {tree[i]} -> {tree[(i - 1) // 2]}")
    i -= 1    
    
