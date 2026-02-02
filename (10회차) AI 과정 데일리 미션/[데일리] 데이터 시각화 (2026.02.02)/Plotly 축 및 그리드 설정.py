import plotly.graph_objects as go
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name='Sine Wave'))

# 축 및 그리드 설정
fig.update_xaxes(
    title_text="X축 이름",           # 축 제목
    showgrid=True,                 # 그리드 표시 여부
    gridwidth=1,                   # 그리드 선 두께
    gridcolor='LightPink',         # 그리드 선 색상
    zeroline=True,                 # 0 기준선 표시 여부
    zerolinewidth=2,               # 0 기준선 두께
    zerolinecolor='Black',         # 0 기준선 색상
    tickvals=[0, 2.5, 5, 7.5, 10], # 눈금 위치 직접 지정
    ticktext=['Min', '', 'Mid', '', 'Max'] # 눈금에 표시될 텍스트
)

fig.update_yaxes(
    title_text="Y축 이름",
    showgrid=True,
    gridwidth=1,
    gridcolor='LightBlue',
    nticks=10,                     # 눈금 개수 근사치
    range=[-1.5, 1.5]              # 축 범위 설정
)

fig.update_layout(title="축 및 그리드 커스텀 예제")
fig.show()