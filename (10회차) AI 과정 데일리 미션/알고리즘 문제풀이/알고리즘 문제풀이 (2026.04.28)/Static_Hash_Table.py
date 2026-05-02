# 해시테이블 클래스 만들기
print("================================")
print("HashTable 클래스: 기본 함수 hash를 이용하기")
print("================================")
# HashTable 클래스: 해시 테이블을 구현 (충돌 처리: 체이닝 방식)
class HashTable:
    # 해시 테이블 초기화
    def __init__(self, length=5):
        self.max_len = length  # 해시 테이블의 최대 길이 (버킷 수)
        self.table = [[] for _ in range(self.max_len)]  # 각 인덱스에 빈 리스트(체인)를 할당
        
    # 해시 함수: 키를 해시 값으로 변환 (문자열의 ASCII 합을 최대 길이로 나눔)
    def _hash(self, key):
        res = sum([ord(s) for s in key])  # 키의 각 문자의 ASCII 값을 합산
        return res % self.max_len  # 합을 최대 길이로 나눈 나머지를 인덱스로 반환
    
    # set(key, value): 키-값 쌍을 해시 테이블에 삽입 (충돌 시 체인에 추가)
    def set(self, key, value):
        index = self._hash(key)  # 키에 대한 해시 인덱스 계산
        self.table[index].append((key, value))  # 해당 인덱스의 체인에 (키, 값) 튜플 추가
        
    # get(key): 키에 해당하는 값을 검색하여 반환
    def get(self, key):
        index = self._hash(key)  # 키에 대한 해시 인덱스 계산
        value = self.table[index]  # 해당 인덱스의 체인(리스트) 가져옴
        if not value:  # 체인이 비어있으면 (키가 존재하지 않음)
            return None
        for v in value:  # 체인을 순회하며 키 일치하는 값 찾기
            if v[0] == key:  # 튜플의 첫 번째 요소(키)가 일치하면
                return v[1]  # 두 번째 요소(값) 반환
        return None  # 체인에 키가 없으면 None 반환
    
if __name__ == "__main__":
    # 해시 테이블 객체 생성 (기본 길이 5)
    capital = HashTable()
    
    # 국가와 수도 데이터 준비
    country = ["Korea", "Japan", "China", "USA", "UK", "France"]
    city = ["Seoul", "Tokyo", "Beijing", "Washington", "London", "Paris"]
    
    # 데이터 삽입: 각 국가를 키로, 수도를 값으로 해시 테이블에 저장
    for co, ci in zip(country, city):
        capital.set(co, ci)
        
    # 해시 테이블의 현재 상태 출력 (각 인덱스의 체인 내용 표시)
    print("해시 테이블의 상태")
    print("======================")
    for i, v in enumerate(capital.table):
        print(f"index {i} : {v}")
    print("======================")
    
    # 해시 테이블 검색 결과 출력 (각 국가의 수도 검색)
    print("해시 테이블의 검색 결과")
    print("======================")
    print(f"Capital of Korea : {capital.get('Korea')}")
    print(f"Capital of Japan : {capital.get('Japan')}")
    print(f"Capital of China : {capital.get('China')}")
    print(f"Capital of USA : {capital.get('USA')}")
    print(f"Capital of UK : {capital.get('UK')}")
    print(f"Capital of France : {capital.get('France')}")
    
print("\n\n")
print("================================")
print("HashTable 클래스: 내장 함수 hash를 이용하기")
print("================================")
class HashTable:
    # 해시 테이블 초기화
    def __init__(self, length=5):
        self.max_len = length  # 해시 테이블의 최대 길이 (버킷 수)
        self.table = [[] for _ in range(self.max_len)]  # 각 인덱스에 빈 리스트(체인)를 할당
            
        
    # set(key, value): 키-값 쌍을 해시 테이블에 삽입 (충돌 시 체인에 추가)
    def set(self, key, value):
        index = hash(key) % self.max_len  # 키에 대한 해시 인덱스 계산
        self.table[index].append((key, value))  # 해당 인덱스의 체인에 (키, 값) 튜플 추가
            
    # get(key): 키에 해당하는 값을 검색하여 반환
    def get(self, key):
        index = hash(key) % self.max_len  # 키에 대한 해시 인덱스 계산
        value = self.table[index]  # 해당 인덱스의 체인(리스트) 가져옴
        if not value:  # 체인이 비어있으면 (키가 존재하지 않음)
            return None
        for v in value:  # 체인을 순회하며 키 일치하는 값 찾기
            if v[0] == key:  # 튜플의 첫 번째 요소(키)가 일치하면
                return v[1]  # 두 번째 요소(값) 반환
        return None  # 체인에 키가 없으면 None 반환
        
if __name__ == "__main__":
    # 해시 테이블 객체 생성 (기본 길이 5)
    capital = HashTable()
    
    # 국가와 수도 데이터 준비
    country = ["Korea", "Japan", "China", "USA", "UK", "France"]
    city = ["Seoul", "Tokyo", "Beijing", "Washington", "London", "Paris"]
    
    # 데이터 삽입: 각 국가를 키로, 수도를 값으로 해시 테이블에 저장
    for co, ci in zip(country, city):
        capital.set(co, ci)
        
    # 해시 테이블의 현재 상태 출력 (각 인덱스의 체인 내용 표시)
    print("해시 테이블의 상태")
    print("======================")
    for i, v in enumerate(capital.table):
        print(f"index {i} : {v}")
    print("======================")
    
    # 해시 테이블 검색 결과 출력 (각 국가의 수도 검색)
    print("해시 테이블의 검색 결과")
    print("======================")
    print(f"Capital of Korea : {capital.get('Korea')}")
    print(f"Capital of Japan : {capital.get('Japan')}")
    print(f"Capital of China : {capital.get('China')}")
    print(f"Capital of USA : {capital.get('USA')}")
    print(f"Capital of UK : {capital.get('UK')}")
    print(f"Capital of France : {capital.get('France')}")
    
print("\n\n")
print("================================")
print("HashTable 클래스: 키가 중복될때 값을 업데이트하기")
print("================================")
class HashTable:
    # 해시 테이블 초기화
    def __init__(self, length=5):
        self.max_len = length  # 해시 테이블의 최대 길이 (버킷 수)
        self.table = [[] for _ in range(self.max_len)]  # 각 인덱스에 빈 리스트(체인)를 할당
        
    # 해시 함수: 키를 해시 값으로 변환 (문자열의 ASCII 합을 최대 길이로 나눔)
    def _hash(self, key):
        res = sum([ord(s) for s in key])  # 키의 각 문자의 ASCII 값을 합산
        return res % self.max_len  # 합을 최대 길이로 나눈 나머지를 인덱스로 반환
    
    # set(key, value): 키-값 쌍을 해시 테이블에 삽입 (충돌 시 체인에 추가)
    def set(self, key, value):
        index = hash(key) % self.max_len  # 키에 대한 해시 인덱스 계산
        for i, (k, v) in enumerate(self.table[index]):  # 해당 인덱스의 체인 순회
            if k == key:  # 키가 이미 존재하면
                self.table[index][i] = (key, value)  # 기존 튜플을 새로운 (키, 값) 튜플로 업데이트
                return
        self.table[index].append((key, value))  # 해당 인덱스의 체인에 (키, 값) 튜플 추가
        
    # get(key): 키에 해당하는 값을 검색하여 반환
    def get(self, key):
        index = self._hash(key)  # 키에 대한 해시 인덱스 계산
        value = self.table[index]  # 해당 인덱스의 체인(리스트) 가져옴
        if not value:  # 체인이 비어있으면 (키가 존재하지 않음)
            return None
        for v in value:  # 체인을 순회하며 키 일치하는 값 찾기
            if v[0] == key:  # 튜플의 첫 번째 요소(키)가 일치하면
                return v[1]  # 두 번째 요소(값) 반환
        return None  # 체인에 키가 없으면 None 반환
    
if __name__ == "__main__":
    # 해시 테이블 객체 생성 (기본 길이 5)
    capital = HashTable()
    
    # 국가와 수도 데이터 준비
    country = ["Korea", "Japan", "China", "USA", "UK", "France"]
    city = ["Seoul", "Tokyo", "Beijing", "Washington", "London", "Paris"]
    
    # 데이터 삽입: 각 국가를 키로, 수도를 값으로 해시 테이블에 저장
    for co, ci in zip(country, city):
        capital.set(co, ci)
        
    # 해시 테이블의 현재 상태 출력 (각 인덱스의 체인 내용 표시)
    print("해시 테이블의 상태")
    print("======================")
    for i, v in enumerate(capital.table):
        print(f"index {i} : {v}")
    print("======================")
    
    # 해시 테이블 검색 결과 출력 (각 국가의 수도 검색)
    print("해시 테이블의 검색 결과")
    print("======================")
    print(f"Capital of Korea : {capital.get('Korea')}")
    print(f"Capital of Japan : {capital.get('Japan')}")
    print(f"Capital of China : {capital.get('China')}")
    print(f"Capital of USA : {capital.get('USA')}")
    print(f"Capital of UK : {capital.get('UK')}")
    print(f"Capital of France : {capital.get('France')}")