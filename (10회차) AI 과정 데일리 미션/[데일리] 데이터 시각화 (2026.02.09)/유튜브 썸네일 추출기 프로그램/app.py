import streamlit as st

st.title("▶️ 유튜브 썸네일 추출기")
# 1. 유튜브 영상 URL 입력 받기
url = st.text_input("🔗 URL을 입력해주세요", value="https://www.youtube.com/watch?v=DQmg0isK1ps")
if url:
    try:
        # 2. URL에서 영상 ID 분리하기
        video_id = url.split("v=")[1].split("&")[0]
        # 3. 썸네일 주소 만들기
        img_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        st.success(f"영상 ID를 찾았습니다: {video_id}")
        # 4. 이미지 화면에 출력하기
        st.image(img_url, caption="추출된 썸네일")
        
    except IndexError:
        st.error("주소 형식이 올바르지 않습니다.")