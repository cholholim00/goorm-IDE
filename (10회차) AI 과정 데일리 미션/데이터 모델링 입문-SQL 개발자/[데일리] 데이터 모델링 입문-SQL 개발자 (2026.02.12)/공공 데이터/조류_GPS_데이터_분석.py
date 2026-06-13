import sqlite3
import pandas as pd

# 1. DB 접속
conn = sqlite3.connect("bird_tracking.db")

# ---------------------------------------------------------
# 📊 분석 1: 어떤 새가 가장 멀리 날아갔을까? (총 이동 거리 순위)
# ---------------------------------------------------------
sql_dist = """
SELECT 
    bird_id,
    COUNT(*) as 데이터_수집_건수,
    ROUND(SUM(dist_km), 2) as 총_이동거리_km,
    ROUND(MAX(speed_kmh), 2) as 최고_속도_kmh
FROM Bird_Movements
GROUP BY bird_id
ORDER BY 총_이동거리_km DESC
LIMIT 5;
"""

print("\n🏆 [분석 1] 장거리 비행 챔피언 (Top 5)")
print(pd.read_sql(sql_dist, conn))

# ---------------------------------------------------------
# 📊 분석 2: 새들은 언제 가장 활발하게 움직일까? (시간대별 활동성)
# ---------------------------------------------------------
# strftime('%H', timestamp): 시간(Hour)만 추출하는 SQLite 함수
sql_time = """
SELECT 
    strftime('%H', timestamp) as 시간대,
    COUNT(*) as 관측_건수,
    ROUND(AVG(speed_kmh), 2) as 평균_속도_kmh,
    SUM(CASE WHEN status = 'Flying' THEN 1 ELSE 0 END) as 비행_횟수
FROM Bird_Movements
GROUP BY 시간대
ORDER BY 평균_속도_kmh DESC
LIMIT 5;
"""

print("\n⏰ [분석 2] 가장 바쁜 시간대 (Top 5)")
print(pd.read_sql(sql_time, conn))

# ---------------------------------------------------------
# 📊 분석 3: '서식지(Resting)' 추정 (많이 머무른 장소)
# ---------------------------------------------------------
# 위도/경도를 소수점 2자리로 잘라서(약 1km 반경) 그룹핑
sql_habitat = """
SELECT 
    ROUND(latitude, 2) as 위도_구역,
    ROUND(longitude, 2) as 경도_구역,
    COUNT(*) as 체류_시간_분,
    bird_id as 대표_개체
FROM Bird_Movements
WHERE status = 'Resting'  -- 쉬고 있는 상태만
GROUP BY 위도_구역, 경도_구역
ORDER BY 체류_시간_분 DESC
LIMIT 5;
"""

print("\n🏠 [분석 3] 주요 서식지/휴식처 추정 (Top 5)")
print(pd.read_sql(sql_habitat, conn))

conn.close()