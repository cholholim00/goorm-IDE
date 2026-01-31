import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1. 데이터 준비
# 샘플 데이터 생성
df = pd.DataFrame({
    'x_val': [1, 2, 3, 4, 5, 10, 20],
    'y_val': [10, 15, 13, 17, 22, 50, 90]
})
# 기본 그래프 생성
fig = px.scatter(df, x='x_val', y='y_val', title="Plotly Axis Practice")

# 2. x축과 y축 설정
# 파라미터: range=[min, max]
# X축 범위를 0부터 10까지, Y축 범위를 0부터 60까지로 제한
fig.update_xaxes(range=[0, 10])
fig.update_yaxes(range=[0, 60])
# (참고) 레이아웃 전체 업데이트 방식을 선호할 경우
# fig.update_layout(xaxis_range=[0, 10], yaxis_range=[0, 60])

# 3. 축 삭제 및 숨김 (Delete / Hide)
# 파라미터: visible=False

# A. 축 전체 숨김
# # X축 전체 숨기기
# fig.update_xaxes(visible=False)
# # Y축 전체 숨기기
# fig.update_yaxes(visible=False)

# B. 축 눈금선 및 틱 라벨 숨김 (Hide Ticks and Tick Labels)
# showgrid=False: 격자(Grid) 숨김
# showticklabels=False: 축의 숫자(라벨) 숨김
# zeroline=False: 0점 기준선 숨김

# Y축의 격자와 숫자만 숨기고, 축의 선(line)은 남기기
fig.update_yaxes(
    showgrid=False,       # 격자 끄기
    showticklabels=False, # 숫자 라벨 끄기
    showline=True,        # 축의 테두리 선은 켜기
    linewidth=2,          # 선 굵기
    linecolor='black'     # 선 색상
)

# 4. 축 수정 및 커스터마이징 (Modify)
# 제목 변경: title_text, title_font
# 눈금 설정: tickvals (특정 위치), dtick (간격), ticktext (표시 텍스트)
# 축 타입 변경: type ('log', 'date', 'category' 등)
# 축 위치 변경: side ('top', 'right' 등)
fig.update_xaxes(
    title_text="Custom X Axis Title", # 축 제목
    title_font=dict(size=18, color='blue'), # 제목 폰트 설정
    tickangle=45,                     # 눈금 텍스트 45도 회전
    showgrid=True,
    gridcolor='lightgray'             # 그리드 색상 변경
)

# Y축을 로그 스케일로 변경하고 오른쪽으로 이동
fig.update_yaxes(
    type="log",    # 로그 스케일
    side="right",  # 축을 오른쪽으로 이동
    title_text="Log Scale Y"
)

# 5. 그래프 출력
fig.show()

# =======================================================================================
# # 종합 실습 코드
# # 1. 데이터 준비
# df = pd.DataFrame({
#     'Day': [1, 2, 3, 4, 5, 6, 7],
#     'Value': [10, 400, 15, 8000, 20, 30, 100000]
# })

# # 2. 기본 그래프 생성
# fig = px.line(df, x='Day', y='Value', title="Plotly Axis Customization Tutorial")

# # 3. X축 커스터마이징 (범위 지정 및 스타일)
# fig.update_xaxes(
#     range=[0.5, 7.5],           # 범위: 0.5 ~ 7.5
#     title_text="영업일 (Day)",   # 제목 설정
#     showgrid=False,             # 세로 격자 숨김
#     linecolor='black',          # 하단 축 선 색상
#     ticks='outside'             # 눈금을 바깥쪽으로 표시
# )

# # 4. Y축 커스터마이징 (로그 스케일 및 포맷)
# fig.update_yaxes(
#     type="log",                 # 로그 스케일 적용 (데이터 편차가 클 때 유용)
#     title_text="매출액 (Log Scale)",
#     tickformat=",",             # 천 단위 콤마 표시
#     gridcolor='lightgray',      # 가로 격자 색상
#     zeroline=True,              # 0점 기준선 표시
#     zerolinecolor='red'         # 0점 기준선 색상
# )

# # 5. 그래프 출력
# fig.show()