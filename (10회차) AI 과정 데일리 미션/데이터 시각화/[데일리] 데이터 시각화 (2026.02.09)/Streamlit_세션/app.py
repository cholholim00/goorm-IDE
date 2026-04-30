import streamlit as st

st.title("✅  카운터 늘리기 앱")

# 1. 초기화: 'count'라는 키가 메모장에 없으면 0으로 만듭니다.
# (앱이 켜지고 딱 한 번만 실행됨)
if 'count' not in st.session_state:
    st.session_state.count = 0

# 2. 버튼 클릭 시: 메모장에 있는 값을 가져와서 1을 더합니다.
if st.button("카운트 증가"):
    st.session_state.count += 1

# 3. 출력: 메모장에 있는 값을 보여줍니다.
st.write(f"현재 카운트: {st.session_state.count}")