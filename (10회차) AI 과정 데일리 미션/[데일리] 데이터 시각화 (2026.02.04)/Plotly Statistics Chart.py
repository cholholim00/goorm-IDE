# ① 히스토그램 (Histogram) - 데이터의 빈도 분포를 보여줍니다.
import plotly.express as px
df = px.data.tips() # 샘플 데이터

fig = px.histogram(df, x="total_bill", nbins=20, color="sex", marginal="rug")
fig.show()

# ② 박스 플롯 (Box Plot) - 데이터의 사분위수, 중앙값, 이상치를 한눈에 파악할 때 필수적입니다.
fig = px.box(df, x="day", y="total_bill", color="smoker", points="all")
fig.show()

# ③ 바이올린 플롯 (Violin Plot) - 박스 플롯에 데이터의 밀도(Density) 곡선을 추가하여 분포 형태를 더 자세히 보여줍니다.
fig = px.violin(df, y="total_bill", x="smoker", color="sex", box=True, points="all")
fig.show()