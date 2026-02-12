import streamlit as st
import time

st.title("⚡️ 빠르게 캐싱앱 이용하기 ")

# [핵심] 이 데코레이터를 붙이면 결과를 저장합니다!
@st.cache_data
def heavy_computation():
    st.write("계산 시작 (처음에만 보입니다)")
    time.sleep(5) 
    return "계산 완료!"

if st.button("계산하기"):
    st.write("버튼 클릭됨!")
    result = heavy_computation()
    st.success(result)