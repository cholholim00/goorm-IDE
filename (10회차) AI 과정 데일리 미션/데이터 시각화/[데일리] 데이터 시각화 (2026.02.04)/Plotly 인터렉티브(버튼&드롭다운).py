import plotly.graph_objects as go
import numpy as np

# 데이터 생성
x = np.linspace(0, 10, 50)
y = np.sin(x)

fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines', name='Sine')])

# 버튼/드롭다운 추가
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons", # 드롭다운으로 바꾸려면 "dropdown"으로 변경
            direction="left",
            buttons=list([
                dict(
                    args=[{"mode": "lines"}],
                    label="Line Chart",
                    method="restyle" # 데이터 속성 변경 시 사용
                ),
                dict(
                    args=[{"mode": "markers"}],
                    label="Scatter Chart",
                    method="restyle"
                ),
                dict(
                    args=[{"type": "bar"}],
                    label="Bar Chart",
                    method="restyle"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11, xanchor="left", y=1.1, yanchor="top"
        ),
    ]
)
fig.show()