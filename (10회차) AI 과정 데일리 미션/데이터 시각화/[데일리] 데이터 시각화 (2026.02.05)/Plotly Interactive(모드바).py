import plotly.express as px

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", log_x=True, title="Mode Bar Customization")

# 제거할 버튼 목록 정의
remove_buttons = ['zoomIn2d', 'zoomOut2d', 'lasso2d']

# 설정 적용하여 출력
fig.show(config={
    'displayModeBar': True,           # 모드 바 표시
    'displaylogo': False,             # Plotly 로고 숨기기
    'modeBarButtonsToRemove': remove_buttons # 특정 버튼 제거
})