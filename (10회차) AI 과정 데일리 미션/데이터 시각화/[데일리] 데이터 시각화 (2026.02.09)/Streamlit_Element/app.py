import streamlit as st
from streamlit_elements import elements, mui, html

st.title("Streamlit Elements 예시")

with elements("new_element"):
    # MUI 카드 컴포넌트 사용
    with mui.Card(variant="outlined", sx={"padding": 2}):
        mui.Typography("이것은  UI 카드입니다", variant="h5")
        mui.Typography("Streamlit 안에서 React 컴포넌트처럼 작동합니다.")
        mui.Button("클릭하세요", variant="contained", color="primary")
        