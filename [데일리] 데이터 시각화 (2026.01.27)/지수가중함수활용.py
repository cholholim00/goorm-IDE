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

    # 3. [전처리] 시계열 분석을 위한 정렬 및 중복 처리
    # 국가별, 연도별로 정렬되어야 EWM(지수가중평균)이 정확하게 계산됩니다.
    # 동일 연도/국가 데이터는 평균으로 통합합니다.
    df = df.groupby(['Country', 'Year', 'Region'], as_index=False).mean()
    df = df.sort_values(by=['Country', 'Year']).reset_index(drop=True)

    # 4. [Groupby 파라미터 활용] 다중 통계량 계산 (미션 1)
    # 각 국가별로 기대수명의 평균과 유병률의 최대치를 요약합니다.
    summary = df.groupby('Country').agg({
        'Life Expectancy': 'mean',
        'Disease Prevalence (%)': ['min', 'max', 'mean']
    })
    print("\n--- [미션 1] 국가별 그룹화 요약 결과 ---")
    print(summary.head())

    # 5. [지수가중함수(EWM) 활용] (미션 2)
    # 국가별로 유병률(Disease Prevalence)의 지수가중이동평균을 구합니다.
    # span=3: 최근 데이터에 더 높은 가중치를 부여합니다.
    df['Disease_EWM'] = df.groupby('Country')['Disease Prevalence (%)'].transform(
        lambda x: x.ewm(span=3, adjust=False).mean()
    )

    print("\n--- [미션 2] EWM 계산 완료 (상위 5행) ---")
    print(df[['Country', 'Year', 'Disease Prevalence (%)', 'Disease_EWM']].head())

    # 6. 결과 시각화
    # 분석할 국가 선택 (예: Germany)
    target_country = 'Germany'
    plot_df = df[df['Country'] == target_country]

    if not plot_df.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(plot_df['Year'], plot_df['Disease Prevalence (%)'], 'o--', label='Original', alpha=0.4)
        plt.plot(plot_df['Year'], plot_df['Disease_EWM'], 'r-s', label=f'EWM Trend (Span=3)', linewidth=2)
        
        plt.title(f'Health Trend Analysis: {target_country}', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Disease Prevalence (%)')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.show()
        print(f"\n✅ {target_country}에 대한 시각화 그래프가 생성되었습니다.")
    else:
        print(f"\n⚠️ {target_country} 데이터를 찾을 수 없습니다.")