import csv

# [준비] 실습용 CSV 파일 만들기 (이 코드를 먼저 한 번 실행하세요)
data = [
    ['이름', '나이', '직업'],
    ['김철수', '25', '개발자'],
    ['이영희', '30', '디자이너']
]

# 'w'는 쓰기 모드 (encoding='utf-8'은 한글 깨짐 방지)
with open('test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("test.csv 파일이 생성되었습니다.\n")


# [실전] CSV 파일 읽기
# 'r'은 읽기 모드
with open('test.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # 한 줄씩 꺼내서 출력하기
    for row in reader:
        print(row)
        
# 출력 결과:
# ['이름', '나이', '직업']
# ['김철수', '25', '개발자']
# ['이영희', '30', '디자이너']

# [추가] 특정 열만 출력하기 (예: 이름 열)
print("\n이름 열만 출력:")
with open('test.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        print(row[0])  # 이름 열 출력
# 출력 결과:
# 김철수
# 이영희

# [추가] 딕셔너리 형태로 읽기
print("\n딕셔너리 형태로 읽기:")
with open('test.csv', 'r', encoding='utf-8') as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        print(row)
# 출력 결과:
# {'이름': '김철수', '나이': '25', '직업': '개발자'}
# {'이름': '이영희', '나이': '30', '직업': '디자이너'}

# [추가] 딕셔너리 형태로 특정 열만 출력하기 (예: 나이 열)
print("\n나이 열만 출력:")
with open('test.csv', 'r', encoding='utf-8') as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        print(row['나이'])  # 나이 열 출력
# 출력 결과:
# 25
# 30