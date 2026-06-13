import sqlite3
import pandas as pd

# 1. DB 접속
conn = sqlite3.connect("seoul_market.db")

# 2. 분석 시나리오: "주말에 사람이 더 많이 몰리는 '핫플레이스' 상권 찾기"
# (평일보다 주말 유동인구가 더 많은 상권을 찾고, 그곳의 매출을 확인합니다)
sql = """
SELECT 
    T.year_quarter as 분기,
    T.market_name as 상권명,
    
    -- [교통] 평일 vs 주말 유동인구 비교
    ROUND(T.weekday_avg, 0) as 평일_평균,
    ROUND(T.weekend_avg, 0) as 주말_평균,
    
    -- [분석] 주말 혼잡도 (주말 / 평일 비율)
    ROUND((T.weekend_avg / T.weekday_avg) * 100, 1) as 주말_활성도_퍼센트,
    
    -- [매출] 해당 상권의 총 매출 (단위: 억)
    ROUND(SUM(S.total_sales) / 100000000.0, 1) as 총매출_억원

FROM Refined_Traffic T
JOIN Market_Sales S 
    ON T.market_code = S.market_code 
    AND T.year_quarter = S.year_quarter

-- 조건: 평일보다 주말에 사람이 더 많은 곳만 필터링 (주말 > 평일)
WHERE T.weekend_avg > T.weekday_avg

GROUP BY T.market_name
ORDER BY 주말_활성도_퍼센트 DESC
LIMIT 15;
"""

# 3. 결과 출력
try:
    df_result = pd.read_sql(sql, conn)
    print("📊 주말 핫플레이스 상권 Top 15 (주말 활성도 순):")
    print(df_result)
except Exception as e:
    print(f"오류 발생: {e}")

conn.close()