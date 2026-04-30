import pandas as pd

# ---------------------------------------------------------
# 0. 데이터 불러오기 (Data Loading)
# ---------------------------------------------------------
# CSV 파일을 읽어옵니다. 파일명이 다르면 'heart_disease_uci.csv' 등으로 고쳐주세요.
df = pd.read_csv('heart.csv') 

print(f"▶ 데이터 로드 완료: 총 {len(df)}행, 컬럼 {df.shape[1]}개")
# 데이터가 잘 들어왔는지 눈으로 확인하기 위해 상위 3줄만 출력합니다.
print(df.head(3)) 


# ---------------------------------------------------------
# 1. insert: 새로운 열(Column) 끼워넣기
# ---------------------------------------------------------
# [목표] 나이(age) 정보를 이용해서 'Age_Group'이라는 그룹을 만들어 봅니다.
# 리스트 컴프리헨션(반복문)을 사용: 50세 이상이면 'Senior', 아니면 'Junior'
age_group = ['Senior' if x >= 50 else 'Junior' for x in df['age']]

# [설명] insert(넣을위치, 새컬럼이름, 넣을데이터)
# loc=1: 0번(id) 다음, 1번(age) 바로 뒤에 넣겠다는 뜻입니다.
df.insert(loc=2, column='Age_Group', value=age_group)

print("\n" + "="*50)
print("1. [insert] Age_Group 컬럼이 age 뒤에 잘 들어갔는지 확인")
print(df[['age', 'Age_Group']].head(3)) # 확인을 위해 두 컬럼만 뽑아서 출력


# ---------------------------------------------------------
# 2. copy: 원본 데이터 보호하기 (Deep Copy)
# ---------------------------------------------------------
# [목표] 이제부터 데이터를 삭제(`pop`, `drop`)할 건데, 원본(`df`)은 남겨두고 싶습니다.
# 그냥 df_clean = df 라고 하면 원본도 같이 지워지므로, 반드시 .copy()를 씁니다.
df_clean = df.copy()

print("\n" + "="*50)
print("2. [copy] df_clean 복사본 생성 완료 (이제 마음껏 지워도 됨)")


# ---------------------------------------------------------
# 3. pop: 정답 데이터 쏙 뽑아내기
# ---------------------------------------------------------
# [목표] 머신러닝 모델에 정답(심장병 유무)을 알려주면 안 되니까 분리합니다.
# 아까 에러가 났던 이유: 데이터셋의 정답 컬럼 이름이 'target'이 아니라 'num'이었습니다.
# pop은 데이터를 반환하면서 동시에 df_clean에서는 삭제해버립니다.
y_label = df_clean.pop('num') 

print("\n" + "="*50)
print("3. [pop] 정답(num) 컬럼 분리 완료")
print(f"- df_clean에 남은 컬럼들: {df_clean.columns.tolist()}") # 'num'이 없어야 정상
print(f"- 따로 챙겨둔 정답 데이터 개수: {len(y_label)}")


# ---------------------------------------------------------
# 4. drop / truncate: 필요 없는 데이터 잘라내기
# ---------------------------------------------------------
# [목표 1] 'id' 컬럼은 환자 번호일 뿐 분석에 쓸모가 없으니 버립니다.
# axis=1: '열(세로)'을 지운다는 뜻 (axis=0은 행/가로 삭제)
if 'id' in df_clean.columns: # 혹시 id 컬럼이 있다면 삭제
    df_clean = df_clean.drop('id', axis=1)

# [목표 2] 데이터가 너무 많다고 가정하고, 연습 삼아 5명만 남기고 싹둑 자릅니다.
# truncate(after=4): 인덱스 4번(5번째 사람) 뒤로는 다 잘라버림
df_mini = df_clean.truncate(after=4)

print("\n" + "="*50)
print("4. [drop/truncate] id 삭제 및 상위 5행만 남기기")
print(df_mini)


# ---------------------------------------------------------
# 5. concat: 데이터 합치기 (블록 조립)
# ---------------------------------------------------------
# [목표] 쪼개진 데이터를 다시 하나로 합치는 연습입니다.
# 먼저 5명을 2명(group_A)과 3명(group_B)으로 나눕니다.
group_A = df_mini.iloc[0:2] 
group_B = df_mini.iloc[2:5] 

# [설명] pd.concat([리스트])
# ignore_index=True: 합칠 때 0, 1, 0, 1... 이렇게 인덱스가 꼬이지 않게 0, 1, 2, 3, 4로 싹 정리해줌
df_concat = pd.concat([group_A, group_B], ignore_index=True)

print("\n" + "="*50)
print("5. [concat] 2명 + 3명 다시 합체 완료")
print(df_concat)


# ---------------------------------------------------------
# 6. drop_duplicates: 중복 데이터 청소하기
# ---------------------------------------------------------
# [목표] 같은 사람이 두 번 기록된 실수를 가정하고 중복을 제거합니다.

# 1. 억지로 중복 만들기: 첫 번째 사람 데이터를 맨 뒤에 한 번 더 붙임
df_dirty = pd.concat([df_concat, df_concat.iloc[[0]]], ignore_index=True)
print("\n" + "="*50)
print(f"6-1. [중복생성] 데이터 개수: {len(df_dirty)} (마지막에 1명 추가됨)")

# 2. 중복 제거하기
# keep='first': 중복된 게 있으면 '첫 번째' 것만 남기고 뒤에 나온 건 지워라
# inplace=True: 따로 변수에 저장하지 않고 `df_dirty` 자체를 바로 수정해라
df_dirty.drop_duplicates(keep='first', inplace=True)

print(f"6-2. [drop_duplicates] 청소 후 개수: {len(df_dirty)} (원상 복구됨)")