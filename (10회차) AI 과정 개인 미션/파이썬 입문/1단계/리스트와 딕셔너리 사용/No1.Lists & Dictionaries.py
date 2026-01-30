# [리스트] - 순서가 있는 데이터의 집합입니다. 대괄호 []를 사용합니다.
# 생성 및 접근
fruits = ['사과', '바나나', '체리']
print(fruits[0])  # 첫 번째 요소 출력: 사과
print(fruits[-1])  # 뒤에서 첫 번째 요소 출력: 체리

# 추가 및 수정 및 삭제
fruits.append('오렌지')  # 맨 뒤에 요소 추가
fruits[1] = '블루베리'  # 인덱스 1의 요소를 '블루베리'로 수정
fruits.insert(1, '포도')  # 특정위치 인덱스 1에 '포도'요소 삽입
del fruits[2]  # 인덱스 2의 요소 삭제
removed_fruit = fruits.pop()  # 맨 뒤의 요소를 제거하고 반환
print(removed_fruit)  # 제거된 요소 출력: 오렌지


# [딕셔너리] - key-value 쌍으로 이루어진 데이터의 집합입니다. 중괄호 {}를 사용합니다.
# 생성 및 접근
student = {
    '이름': '홍길동',
    '나이': 20,
    '전공': '컴퓨터공학'
}
print(student['이름'])  # '이름' 키의 값 출력: 홍길동
student['지역'] = '서울'  # 새로운 키-값 쌍 추가
print(student.keys())  # 모든 키 출력
print(student.values())  # 모든 값 출력
print(student.items())  # 모든 키-값 쌍 출력

# 수정 및 삭제
student['나이'] = 26 # '나이' 키의 값을 26으로 수정
del student['지역']  # '지역' 키-값 쌍 삭제
removed_value = student.pop('전공')  # '전공' 키-값 쌍 제거 및 값 반환
print(removed_value)  # 제거된 값 출력: 컴퓨터공학


