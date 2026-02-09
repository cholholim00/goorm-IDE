import pandas as pd
import os

# 1. 파일 경로
base_path = os.path.dirname(os.path.abspath(__file__))
daily_out = os.path.join(base_path, 'data', 'daily_covid_data.csv')
regional_out = os.path.join(base_path, 'data', 'regional_covid_data.csv')

# 원본 파일
file_daily = '일별_발생_성별_통합.csv'
file_vac = '예방접종_통계_현황_통합.csv'
file_region = '시군구별_월별_확진자_사망_발생현황_통합.csv'

def process_data_v4():
    print("🚀 [Final] A/B/C팀 모든 요구사항을 반영하여 데이터를 구축합니다...")

    # -------------------------------------------------------
    # 1. [A팀 & C팀용] 일별 데이터 (확진/사망 + 백신)
    # -------------------------------------------------------
    try:
        print("   -> 1단계: 일별 데이터 통합 중...")
        # 확진/사망 로드
        df = pd.read_csv(os.path.join(base_path, file_daily))
        df['date'] = pd.to_datetime(df['날짜'])
        
        # A팀 컬럼 생성
        df['new_cases'] = df['국내발생'] + df['해외유입']
        df['new_deaths'] = df['사망']
        df = df.sort_values('date')
        df['cum_cases'] = df['new_cases'].cumsum()
        df['cum_deaths'] = df['new_deaths'].cumsum()
        
        df_daily = df[['date', 'new_cases', 'new_deaths', 'cum_cases', 'cum_deaths']]

        # 백신 로드 및 병합
        if os.path.exists(os.path.join(base_path, file_vac)):
            df_v = pd.read_csv(os.path.join(base_path, file_vac))
            df_v = df_v[df_v['지표'] == '건수']
            df_v['date'] = pd.to_datetime(df_v['날짜'])
            
            # 일별 합계 -> 누적 합계
            v_grp = df_v.groupby('date')['값'].sum().reset_index()
            v_grp.columns = ['date', 'cnt']
            v_grp['accumulated_vaccine_count'] = v_grp['cnt'].cumsum()
            
            df_daily = pd.merge(df_daily, v_grp[['date', 'accumulated_vaccine_count']], on='date', how='left')
            df_daily = df_daily.fillna(0)
        
        # 저장
        os.makedirs(os.path.dirname(daily_out), exist_ok=True)
        df_daily.to_csv(daily_out, index=False, encoding='utf-8-sig')
        print(f"   ✅ daily_covid_data.csv 생성 완료 ({len(df_daily)}행)")

    except Exception as e:
        print(f"❌ 1단계 오류: {e}")

    # -------------------------------------------------------
    # 2. [B팀용] 지역별 데이터 (Wide Format 변환)
    # -------------------------------------------------------
    try:
        print("   -> 2단계: B팀용 지역 데이터 변환 중 (Pivoting)...")
        df_r = pd.read_csv(os.path.join(base_path, file_region))
        df_r['date'] = pd.to_datetime(df_r['날짜'])
        
        # '확진자'만 필터링 (사망자 제외)
        df_r = df_r[df_r['유형'] == '확진자']
        
        # 피벗 테이블 생성 (행: 날짜, 열: 시도명, 값: 합계)
        # B팀 코드는 컬럼에 '서울', '부산' 등이 있어야 함
        df_wide = df_r.pivot_table(index='date', columns='시도명', values='값', aggfunc='sum').reset_index()
        df_wide = df_wide.fillna(0)
        
        # 저장
        df_wide.to_csv(regional_out, index=False, encoding='utf-8-sig')
        print(f"   ✅ regional_covid_data.csv 생성 완료 ({len(df_wide)}행, Wide Format)")

    except Exception as e:
        print(f"❌ 2단계 오류: {e}")

    print("\n" + "="*50)
    print("🎉 [데이터 준비 완료] main.py를 실행하세요!")
    print("="*50)

if __name__ == "__main__":
    process_data_v4()