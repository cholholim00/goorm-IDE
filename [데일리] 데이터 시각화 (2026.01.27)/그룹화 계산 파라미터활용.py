import pandas as pd
import numpy as np

# 가상의 의료/시계열 데이터 생성
data = {
    '날짜': pd.to_datetime(['2026-01-01', '2026-01-01', '2026-01-02', '2026-01-02', '2026-01-03']),
    '병원_ID': ['병원A', '병원B', '병원A', '병원B', '병원A'],
    '환자수': [10, 20, 15, 25, 12],
    '운영비용': [100, 200, 150, 220, 130]
}
df = pd.DataFrame(data)

# groupby 파라미터 활용
grouped = df.groupby('병원_ID').agg({ # agg()를 활용한 다중 통계량 산출
    '환자수': ['sum', 'mean'],     # 한 번의 그룹화로 합계와 평균을 동시에 계산
    '운영비용': lambda x: x.max() - x.min()  # 사용자 정의 함수 (변동폭)
})

# as_index=False: 그룹 키를 인덱스가 아닌 컬럼으로 유지 (시각화할 때 편함)
result = df.groupby('병원_ID', as_index=False)['환자수'].mean()

print("--- 병원별 환자수 평균 분석 결과 ---")
print(result)