import sqlite3
import pandas as pd

# 1. 아까 만든 DB 파일에 접속
# (파일이 같은 폴더에 있어야 합니다)
conn = sqlite3.connect("seoul_market.db")

# 2. 분석하고 싶은 SQL 쿼리 작성
# "상권별로 20대 유동인구와 술집(Pub) 매출의 관계를 보여줘!"
sql = """
SELECT 
    S.year_quarter as 분기,
    S.market_name as 상권명,
    S.service_type as 업종,
    S.total_sales as 총매출,
    P.age_20s_pop as '20대_유동인구',
    (S.total_sales / P.total_pop) as 인당_매출기여도
FROM Market_Sales S
JOIN Market_Population P 
    ON S.market_code = P.market_code 
    AND S.year_quarter = P.year_quarter
WHERE S.service_type LIKE '%호프%' OR S.service_type LIKE '%술집%'
ORDER BY S.total_sales DESC
LIMIT 10;
"""

# 3. SQL 실행 및 결과 보기 (판다스로 예쁘게 출력)
df_result = pd.read_sql(sql, conn)

print("📊 분석 결과 (매출 Top 10):")
print(df_result)

# 4. 연결 종료
conn.close()