import plotly.graph_objects as go
import numpy as np

# 1. 데이터 생성 (이 부분이 누락되었을 가능성이 큽니다!)
x = np.linspace(0, 10, 100)

fig = go.Figure()

# 첫 번째 그래프 추가
fig.add_trace(go.Scatter(x=x, y=np.sin(x), name='Sine', mode='lines'))

# 두 번째 그래프 추가 (겹쳐짐)
fig.add_trace(go.Scatter(x=x, y=np.cos(x), name='Cosine', mode='lines+markers'))

fig.update_layout(title="그래프 겹쳐 그리기")
fig.show()