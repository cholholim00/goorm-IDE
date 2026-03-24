import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image
import sqlite3
import os
from db_manager import get_connection

# 모델 로드 (캐싱하여 속도 최적화)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('model/xray_mobilenetv2_best.h5')

model = load_model()

st.set_page_config(page_title="Hana Medical AI", layout="wide")
st.title("🩻 흉부 X-ray 폐렴 판독 서비스")

# 사이드바: 현재 DB 현황 확인
with st.sidebar:
    st.header("📊 실시간 예약 현황")
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM appointments", conn)
    st.dataframe(df)
    conn.close()

# 메인 화면: 데이터 입력 및 판독
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 사진 업로드")
    uploaded_file = st.file_uploader("환자의 흉부 X-ray 사진을 선택하세요", type=['jpg', 'png', 'jpeg'])
    app_id = st.number_input("예약 번호(App ID) 입력", min_value=1, value=1)

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='업로드된 X-ray', use_container_width=True)
    
    if st.button("🔍 AI 판독 시작"):
        with st.spinner('AI 모델이 영상을 분석 중입니다...'):
            # 2. 이미지 전처리
            img = img.resize((160, 160))  # 모델 규격에 맞게 160으로 수정
            img_array = np.array(img) / 255.0 # 정규화
            img_array = np.expand_dims(img_array, axis=0)

            # 3. 모델 추론
            pred = model.predict(img_array)
            result_idx = 1 if pred[0][0] > 0.5 else 0
            confidence = pred[0][0] if result_idx == 1 else 1 - pred[0][0]
            result_text = "PNEUMONIA (폐렴)" if result_idx == 1 else "NORMAL (정상)"
            
            with col2:
                st.subheader("2. 판독 결과")
                color = "red" if result_idx == 1 else "green"
                st.markdown(f"### 결과: :{color}[{result_text}]")
                st.metric("신뢰도", f"{confidence:.2%}")

                # 4. DB 업데이트
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE appointments SET status='COMPLETED', diagnosis_result=? WHERE app_id=?", 
                           (f"{result_text} ({confidence:.2%})", app_id))
                conn.commit()
                conn.close()
                st.success(f"DB 업데이트 완료! (App ID: {app_id})")