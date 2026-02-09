import plotly.graph_objects as go
import pandas as pd

# 샘플 시계열 데이터 생성
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure()

# 선 그래프 추가
fig.add_trace(go.Scatter(x=df['Date'], y=df['AAPL.Close'], name="Apple Stock"))

# 슬라이더(Range Slider) 추가 및 제목 설정
fig.update_layout(
    title="Apple Stock Price with Range Slider",
    xaxis_title="Date",
    yaxis_title="Price (USD)"
)

# X축에 레인지 슬라이더 활성화
fig.update_xaxes(rangeslider_visible=True)

fig.show()