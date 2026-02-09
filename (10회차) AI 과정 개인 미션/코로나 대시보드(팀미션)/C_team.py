import pandas as pd
import plotly.graph_objects as go
import os

# 1. 데이터 로드 (project_reset.py로 만든 데이터 사용)
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, 'data', 'daily_covid_data.csv')

if not os.path.exists(file_path):
    print("❌ 데이터 파일이 없습니다! 'project_reset.py'를 먼저 실행해주세요.")
    exit()

df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'])

# 2. 데이터 확인 (터미널 출력용)
print(f"📊 데이터 로드 완료: {len(df)}행")
print(f"   - 사망자 컬럼: new_deaths")
print(f"   - 백신 컬럼: accumulated_vaccine_count")

# 3. 그래프 그리기 (이중축)
fig = go.Figure()

# (1) 왼쪽 축: 일일 사망자 (막대 그래프)
fig.add_trace(go.Bar(
    x=df['date'], 
    y=df['new_deaths'], 
    name='일일 사망자', 
    marker_color='#FF7043', # 연한 주황/빨강
    opacity=0.4
))

# (2) 오른쪽 축: 누적 백신 접종 (선 그래프)
fig.add_trace(go.Scatter(
    x=df['date'], 
    y=df['accumulated_vaccine_count'], 
    name='누적 백신 접종', 
    line=dict(color='#FB8C00', width=4), # 진한 주황
    yaxis='y2'
))

# 4. 레이아웃 설정
fig.update_layout(
    title='💉 백신 접종 증가(선)와 사망자 감소(막대)의 상관관계',
    xaxis=dict(title='날짜'),
    
    # 왼쪽 Y축 (사망자)
    yaxis=dict(
        title='일일 사망자 수 (명)', 
        side='left',
        showgrid=True,
        gridcolor='lightgray'
    ),
    
    # 오른쪽 Y축 (백신)
    yaxis2=dict(
        title='누적 백신 접종 수 (건)', 
        overlaying='y', 
        side='right', 
        showgrid=False # 그래프가 지저분해지지 않게 그리드 끔
    ),
    
    template='plotly_white',
    hovermode='x unified', # 마우스 올리면 두 값 동시에 보여줌
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)')
)

print("✅ C팀 그래프 생성 완료! (브라우저가 열립니다)")
fig.show()