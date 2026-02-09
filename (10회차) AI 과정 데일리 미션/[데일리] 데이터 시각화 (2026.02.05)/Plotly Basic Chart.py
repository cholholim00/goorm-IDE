#  시작은 간편하게
import plotly.express as px

# 1. 데이터 로드
df = px.data.iris()

# 2. 기본 차트 생성 (여기에 템플릿을 바로 적용할 수도 있습니다)
fig = px.scatter(df, 
                 x="sepal_width", 
                 y="sepal_length", 
                 color="species",
                 title="Iris Dataset with Custom ModeBar & Dark Theme",
                 template='plotly_dark') # 'plotly_white', 'seaborn' 등 다양한 테마 제공

# 3. 레이아웃(그리기 환경) 디테일 조정
fig.update_layout(
    font=dict(family="Courier New, monospace", size=14, color="white"), # 폰트 설정
    dragmode='pan' # 초기 마우스 모드를 '이동'으로 설정
)

# 4. 모드 바(Mode Bar) 설정: 여기가 핵심입니다!
# 기본적으로 숨겨진 '그리기 도구'들을 추가하고, 불필요한 버튼은 제거합니다.
my_config = {
    'displayModeBar': True,  # 모드 바 항상 표시
    'displaylogo': False,    # Plotly 로고 숨기기
    
    # [추가할 버튼] 선 그리기, 사각형 그리기, 원 그리기, 도형 지우기
    'modeBarButtonsToAdd': [
        'drawline',
        'drawopenpath',
        'drawcircle',
        'drawrect',
        'eraseshape'
    ],
    
    # [제거할 버튼] 라쏘 선택, 박스 선택 등 잘 안 쓰는 기능 제거
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'] 
}

# 5. 설정(config)을 적용하여 출력
fig.show(config=my_config)