import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 경로 설정 (파일을 못 찾는 문제 해결)
# 스크립트 파일이 있는 위치를 기준으로 데이터 파일을 찾습니다.
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, 'global_health_trends.csv')

# 만약 위 방법으로도 안되면, 절대경로를 직접 지정하자
# file_path = "/Users/qwer/Documents/GitHub/goorm-IDE/[데일리] 데이터 시각화 (2026.01.27)/global_health_trends.csv"

if not os.path.exists(file_path):
    print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    print("현재 실행 중인 경로에 'global_health_trends.csv' 파일이 있는지 확인해주세요.")
else:
    # 2. 데이터 불러오기
    df = pd.read_csv(file_path)

  # ---------------------------------------------------------
    # [Mission 1] 데이터 전처리 (Data Preprocessing)
    # ---------------------------------------------------------
    # 1) 동일 국가/연도 데이터가 여러 개 있으므로 평균값으로 통합
    # 2) 시계열 분석(EWM)을 위해 국가별, 연도별 오름차순 정렬
    df_clean = df.groupby(['Country', 'Year', 'Region'], as_index=False).mean()
    df_clean = df.sort_values(by=['Country', 'Year']).reset_index(drop=True)
    
    print("✅ Mission 1: 전처리 및 정렬 완료")

    # ---------------------------------------------------------
    # [Mission 2] 그룹화 계산 파라미터 활용 (Groupby Aggregation)
    # ---------------------------------------------------------
    # agg()를 사용하여 컬럼별로 각각 다른 통계 지표 산출
    # as_index=False를 사용하여 결과가 바로 데이터프레임 형식이 되도록 설정
    summary = df_clean.groupby('Country', as_index=False).agg({
        'Life Expectancy': ['mean', 'std'],            # 기대수명의 평균과 표준편차
        'Disease Prevalence (%)': ['min', 'max']       # 질병 유병률의 최소/최대값
    })
    
    # 멀티 인덱스 컬럼 정리 (Notion에 표로 넣기 좋게 변환)
    summary.columns = ['Country', 'Avg_Life', 'Std_Life', 'Min_Disease', 'Max_Disease']
    
    print("\n--- [✅ Mission 2 결과: 국가별 통계 요약] ---")
    print(summary.head())

   # ---------------------------------------------------------
    # [Mission 3] 지수가중함수 활용 (EWM)
    # ---------------------------------------------------------
    # transform을 활용해 국가별 그룹 내에서 독립적으로 EWM 계산
    # span=3: 최근 데이터에 더 가중치를 두어 유병률의 '최신 트렌드' 파악
    df_clean['Disease_EWM'] = df_clean.groupby('Country')['Disease Prevalence (%)'].transform(
        lambda x: x.ewm(span=3, adjust=False).mean()
    )

    print("\n✅ Mission 3: 지수가중평균(EWM) 계산 완료")

    # ---------------------------------------------------------
    # [데이터 시각화] 결과 확인
    # ---------------------------------------------------------
    # 분석 예시: 독일(Germany)의 유병률 변화 추세
    target_country = 'Germany'
    plot_df = df_clean[df_clean['Country'] == target_country]

    if not plot_df.empty:
        plt.figure(figsize=(12, 6))
        # 원본 데이터 (Raw Data)
        plt.plot(plot_df['Year'], plot_df['Disease Prevalence (%)'],
                  'o--', label='실제 측정값', alpha=0.4)
        # 지수가중평균 데이터 (EWM Trend)          
        plt.plot(plot_df['Year'], plot_df['Disease_EWM'], 
                  'r-s', label='latest trends(EWM)', linewidth=2)
        
        plt.title(f'[{target_country}] 질병 유병률 시계열 분석 (EWM)', fontsize=14)
        plt.xlabel('연도')
        plt.ylabel('유병율(%)')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.show()
        
        print(f"\n✅ {target_country}에 대한 시각화 그래프가 생성되었습니다.")
    else:
        print(f"\n⚠️ {target_country} 데이터를 찾을 수 없습니다.")