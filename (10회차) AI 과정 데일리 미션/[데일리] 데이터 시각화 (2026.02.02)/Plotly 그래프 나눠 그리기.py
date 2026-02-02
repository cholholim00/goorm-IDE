import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 1. 데이터 정의 (이 줄이 반드시 있어야 NameError가 안 납니다!)
x = np.linspace(0, 10, 100) 

# 2. 서브플롯 생성 (1행 2열)
fig = make_subplots(rows=1, cols=2, subplot_titles=("Sine Wave", "Cosine Wave"))

# 3. 첫 번째 칸에 Sine 그래프 추가
fig.add_trace(
    go.Scatter(x=x, y=np.sin(x), name="Sine"),
    row=1, col=1
)

# 4. 두 번째 칸에 Cosine 그래프 추가
fig.add_trace(
    go.Scatter(x=x, y=np.cos(x), name="Cosine"),
    row=1, col=2
)

# 5. 레이아웃 업데이트 및 출력
fig.update_layout(title_text="Plotly 서브플롯 예제", showlegend=False)
fig.show()