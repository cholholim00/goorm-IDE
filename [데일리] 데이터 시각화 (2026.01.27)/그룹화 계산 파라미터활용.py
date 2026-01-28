import pandas as pd
import numpy as np

# 가상의 의료/시계열 데이터 생성
data = {
    'Date': pd.to_datetime(['2026-01-01', '2026-01-01', '2026-01-02', '2026-01-02', '2026-01-03']),
    'Hospital_ID': ['A', 'B', 'A', 'B', 'A'],
    'Patient_Count': [10, 20, 15, 25, 12],
    'Operating_Cost': [100, 200, 150, 220, 130]
}
df = pd.DataFrame(data)

# groupby 파라미터 활용
grouped = df.groupby('Hospital_ID').agg({
    'Patient_Count': ['sum', 'mean'],     # 여러 함수 적용
    'Operating_Cost': lambda x: x.max() - x.min()  # 사용자 정의 함수 (변동폭)
})

# as_index=False: 그룹 키를 인덱스가 아닌 컬럼으로 유지 (시각화할 때 편함)
result = df.groupby('Hospital_ID', as_index=False)['Patient_Count'].mean()
print(result)