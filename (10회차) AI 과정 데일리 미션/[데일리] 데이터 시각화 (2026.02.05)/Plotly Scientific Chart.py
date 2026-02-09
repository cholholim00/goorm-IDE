# 과학적 시각화
import plotly.express as px

# 샘플 데이터 로드 (붓꽃 데이터)
df = px.data.iris()

# 3D 산점도 그리기
fig = px.scatter_3d(df, 
                    x='sepal_length', 
                    y='sepal_width', 
                    z='petal_width',
                    color='species',
                    symbol='species',  # 종별로 마커 모양 다르게
                    opacity=0.7,       # 투명도 조절
                    title="3D Iris Dataset Analysis")

# 레이아웃 조금 더 다듬기 (배경색 등)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))

fig.show()