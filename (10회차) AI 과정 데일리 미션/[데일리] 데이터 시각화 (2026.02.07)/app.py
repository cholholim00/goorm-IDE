import streamlit as st
import pandas as pd

 # 기본 문법
st.title("나의 첫 Streamlit 앱")

# 매직 커맨드: 그냥 변수만 적으면 출력됨
df = pd.DataFrame({'first column': [1, 2, 3, 4]})
df  # 화면에 데이터프레임이 그려짐!

# 정석적인 출력 방법
st.write("st.write()는 마크다운, 데이터, 차트 등 뭐든지 출력합니다.")

# ==========================================================================

# 핵심 컴포넌트
# 1. 버튼
if st.button('Click me'):
    st.write('버튼이 클릭되었습니다!')

# 2. 슬라이더
age = st.slider('나이를 선택하세요', 0, 100, 25)
st.write(f"당신의 나이는 {age}세 입니다.")

# 3. 텍스트 입력
title = st.text_input('영화 제목 입력', 'Inception')
st.write('현재 영화:', title)

# 4. 선택 박스
option = st.selectbox(
    '가장 좋아하는 색상은?',
    ('Red', 'Green', 'Blue'))
st.write('선택:', option)

# ==========================================================================

# 레이아웃 및 폼
# 사이드바: 설정 메뉴 등을 넣기 좋음
st.sidebar.title("설정 메뉴")
user_id = st.sidebar.text_input("ID 입력")

# 컬럼: 화면을 가로로 분할
col1, col2 = st.columns(2)

with col1:
    st.header("왼쪽 구역")
    st.image("https://via.placeholder.com/150")

with col2:
    st.header("오른쪽 구역")
    st.write("여기에 차트나 설명을 넣습니다.")
    
# ==========================================================================

# 인터랙티브 폼
with st.form("my_form"):
    st.write("주문서 작성")
    menu = st.selectbox("메뉴", ["커피", "차", "주스"])
    sugar = st.checkbox("설탕 추가")
    
    # 모든 폼은 submit 버튼이 필수입니다.
    submitted = st.form_submit_button("주문하기")

if submitted:
    st.write(f"주문 내용: {menu}, 설탕: {sugar}")
    
# ==========================================================================