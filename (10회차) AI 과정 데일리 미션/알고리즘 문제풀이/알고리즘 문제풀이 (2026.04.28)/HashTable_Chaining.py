# 분리 연결법 기반의 해시 테이블 충돌해결
class HashTable:
    def __init__(self, size):
        self.size = size
        # 각 버킷을 빈 리스트(Chaining용)로 초기화
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        # 단순한 나머지 연산 해시 함수
        return hash(key) % self.size

    def insert(self, key, value):
        hash_index = self._hash_function(key)
        
        # 이미 키가 존재하면 값 업데이트
        for pair in self.table[hash_index]:
            if pair[0] == key:
                pair[1] = value
                return
        
        # 새로운 키-값 쌍 추가 (Chaining)
        self.table[hash_index].append([key, value])

    def get(self, key):
        hash_index = self._hash_function(key)
        for pair in self.table[hash_index]:
            if pair[0] == key:
                return pair[1]
        return None  # 찾는 키가 없음

    def delete(self, key):
        hash_index = self._hash_function(key)
        for i, pair in enumerate(self.table[hash_index]):
            if pair[0] == key:
                del self.table[hash_index][i]
                return True
        return False

# 테스트
ht = HashTable(10)
ht.insert("name", "Choi")
ht.insert("job", "Developer")
print(f"Name: {ht.get('name')}") # 출력: Choi