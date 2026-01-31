# update_traces 메서드는 그래프의 실제 데이터가 표현되는 방식(점, 선, 막대 등)을 일괄적으로 변경하거나, 특정 조건에 맞는 데이터만 골라서 스타일을 수정할 때 사용
import plotly.express as px
import pandas as pd

# 샘플 데이터 생성 (두 개의 그룹 A, B)
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'y': [10, 15, 13, 17, 22, 5, 8, 7, 9, 12],
    'Group': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
    'Label': ['Low', 'Med', 'Med', 'High', 'Top', 'Low', 'Low', 'Med', 'Med', 'High']
})
# 그룹별로 색상이 다른 기본 그래프 생성
fig = px.scatter(df, x='x', y='y', color='Group', title="Trace Update Practice")

# 2. 마커 스타일 일괄 변경 - 그래프에 있는 모든 점의 크기, 테두리, 투명도 등을 한 번에 변경
# 주요 속성: marker_size, marker_symbol, marker_line_width, marker_opacity
fig.update_traces(
    marker_size=15,              # 점 크기 키우기
    marker_symbol='diamond',     # 점 모양을 다이아몬드로 변경
    marker_line_width=2,         # 점 테두리 두께
    marker_line_color='black',   # 점 테두리 색상
    opacity=0.8                  # 투명도 조절 (0~1)
)

# 3. 호버 및 텍스트 정보 수정 - 마우스를 올렸을 때 나오는 정보(Tooltip)나 데이터 포인트 위에 표시되는 텍스트를 수정
# 주요 속성: hovertemplate, textposition

# 3-1. 텍스트 라벨 추가 (df의 'Label' 컬럼 사용)
# 주의: px.scatter 생성 시 text='Label'을 지정했어야 가장 자연스럽지만, 
# 여기서 강제로 text 모드로 바꿀 수도 있습니다.
fig.update_traces(
    text=df['Label'],           # 데이터 포인트에 표시할 텍스트 지정
    textposition='top center',  # 텍스트 위치 (점 위쪽 가운데)
    mode='markers+text'         # 점과 텍스트를 함께 표시하도록 모드 변경
)
# 3-2. 호버 툴팁 커스터마이징
# %{x}, %{y}는 좌표값, %{text}는 위에서 설정한 라벨
fig.update_traces(
    hovertemplate="<b>X값:</b> %{x}<br><b>Y값:</b> %{y}<br><b>등급:</b> %{text}"
)

# 4. 조건부 업데이트 - 모든 점을 바꾸는 것이 아니라, 특정 그룹(Trace)만 콕 집어서 스타일을 바꾼다.
# 파라미터: selector=dict(...)
# 'Group'이 'B'인 Trace만 찾아서 스타일 변경
fig.update_traces(
    selector=dict(name='B'),     # 범례(name) 이름이 'B'인 trace만 선택
    marker_color='gray',         # 색상을 회색으로 변경
    marker_opacity=0.3           # 흐리게 처리 (비활성화 느낌)
)
# 'Group'이 'A'인 Trace는 강조
fig.update_traces(
    selector=dict(name='A'),
    marker_size=20,
    marker_line_color='red'
)

# 5. 그래프 출력
fig.show()
# ============================================================================================================================
# # 종합 실습 코드
# # 1. 데이터 준비
# df = pd.DataFrame({
#     'x': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
#     'y': [10, 15, 13, 17, 22, 5, 8, 7, 9, 12],
#     'Group': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
#     'Note': ['Start', '', 'Check', '', 'End', '', '', '', '', '']
# })
# # 2. 기본 그래프
# fig = px.scatter(df, x='x', y='y', color='Group', 
#                  title="Advanced Trace Updating",
#                  text='Note') # 텍스트 데이터 미리 연결

# # 3. 전체 공통 스타일 적용 (기본 마커 설정)
# fig.update_traces(
#     marker_size=12,
#     marker_line_width=1,
#     marker_line_color='white'
# )
# # 4. [중요] 그룹 B (배경 역할) 스타일링
# fig.update_traces(
#     selector=dict(name='B'),
#     marker_color='lightgray', # 회색으로 죽이기
#     mode='markers'            # 텍스트 숨기고 마커만 표시
# )
# # 5. [중요] 그룹 A (강조 역할) 스타일링
# fig.update_traces(
#     selector=dict(name='A'),
#     marker_symbol='star',      # 별 모양
#     marker_size=18,            # 크기 강조
#     marker_line_color='black', # 테두리 진하게
#     textposition='top center', # 텍스트 위치
#     textfont_size=14
# )
# # 6. 그래프 출력
# fig.show()