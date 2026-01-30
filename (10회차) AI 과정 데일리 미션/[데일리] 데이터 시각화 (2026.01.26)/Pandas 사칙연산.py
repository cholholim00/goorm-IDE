import pandas as pd
import numpy as np

# 데이터프레임 1
df1 = pd.DataFrame({
    'A': [1, 2],
    'B': [3, 4]
}, index=[0, 1])

# 데이터프레임 2
df2 = pd.DataFrame({
    'B': [10, 20],
    'C': [30, 40]
}, index=[1, 2])

# 1. 산술 연산자 방식
print(">>>>>> + \n", df1 + 5)
print(">>>>>> - \n", df2 - 7)
print(">>>>>> * \n", df1 * 10)
print(">>>>>> / \n", df2 / 15)

# 2. 메서드 방식 (괄호 안에 값 필수!)
print(">>>>>> add \n", df1.add(5))
print(">>>>>> sub \n", df2.sub(7))
print(">>>>>> mul \n", df1.mul(10))
print(">>>>>> div \n", df2.div(15))