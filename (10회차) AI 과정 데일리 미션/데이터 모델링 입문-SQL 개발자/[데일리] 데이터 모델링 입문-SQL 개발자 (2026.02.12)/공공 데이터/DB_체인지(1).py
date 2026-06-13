import pandas as pd
import sqlite3

# 1. 빈 데이터베이스 파일 만들기 (이름: seoul_market.db)
conn = sqlite3.connect("seoul_market.db")

# 2. CSV 파일 읽어오기 (파일명만 정확히 입력하세요)
# (한글 파일은 encoding='cp949' 또는 'utf-8'을 써야 안 깨집니다)
df_pop = pd.read_csv("dataset/서울시 상권분석서비스(길단위인구-상권).csv", encoding='cp949')
df_sales = pd.read_csv("dataset/서울시 상권분석서비스(추정매출-상권).csv", encoding='cp949')

# 3. 보기 편하게 컬럼 이름 영어로 바꾸기 (선택사항이지만 추천!)
df_pop.rename(columns={
    '기준_년분기_코드': 'year_quarter',
    '상권_코드': 'market_code',
    '총_유동인구_수': 'total_pop',
    '연령대_20_유동인구_수': 'age_20s_pop'
}, inplace=True)

df_sales.rename(columns={
    '기준_년분기_코드': 'year_quarter',
    '상권_코드': 'market_code',
    '상권_코드_명': 'market_name',
    '서비스_업종_코드_명': 'service_type',
    '당월_매출_금액': 'total_sales'
}, inplace=True)

# 4. 데이터베이스에 집어넣기 (핵심!)
# to_sql("테이블이름", 연결변수, 옵션)
df_pop.to_sql("Market_Population", conn, if_exists="replace", index=False)
df_sales.to_sql("Market_Sales", conn, if_exists="replace", index=False)

# 5. 저장하고 끝내기
conn.close()
print("데이터베이스 변환 완료!")