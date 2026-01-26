import pandas as pd

# 딕셔너리를 이용한 생성
data = {
    'A': [10, 20, 30],
    'B': [5, 15, 25],
    'C': [1, 2, 3]
}
df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])
print(df)