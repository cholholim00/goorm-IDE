"""
BMI Calculator Streamlit Web Application
"""
import tests.test_health_calculator as test
import streamlit as st
from utils.health_calculator import calculate_bmi

# Page configuration
st.set_page_config(
    page_title="BMI 계산기",
    page_icon="⚕️",
    layout="centered"
)

# Title
st.title("⚕️ BMI 계산기")
st.markdown("---")

# Description
st.markdown("""
### 체질량지수(BMI) 계산
키와 몸무게를 입력하여 BMI를 계산하고 건강 상태를 확인하세요.
""")

# Input section
col1, col2 = st.columns(2)

with col1:
    height = st.number_input(
        "키 (cm)",
        min_value=0.0,
        max_value=300.0,
        value=170.0,
        step=0.1,
        help="키를 센티미터 단위로 입력하세요"
    )

with col2:
    weight = st.number_input(
        "몸무게 (kg)",
        min_value=0.0,
        max_value=500.0,
        value=65.0,
        step=0.1,
        help="몸무게를 킬로그램 단위로 입력하세요"
    )

# Calculate button
if st.button("🔍 계산하기", type="primary", use_container_width=True):
    try:
        # Calculate BMI
        result = calculate_bmi(height, weight)
        
        # Calculate actual BMI value for display
        height_m = height / 100
        bmi_value = weight / (height_m ** 2)
        
        # Display results
        st.markdown("---")
        st.subheader("📊 결과")
        
        # Create columns for results
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            st.metric(label="BMI 수치", value=f"{bmi_value:.2f}")
        
        with result_col2:
            # Color coding based on category
            if result == "저체중":
                st.metric(label="건강 상태", value=result, delta="⚠️")
            elif result == "정상":
                st.metric(label="건강 상태", value=result, delta="✅")
            elif result == "과체중":
                st.metric(label="건강 상태", value=result, delta="⚠️")
            else:  # 비만
                st.metric(label="건강 상태", value=result, delta="🔴")
        
        # BMI information
        st.markdown("---")
        st.markdown("""
        #### 📖 BMI 기준
        - **저체중**: BMI < 18.5
        - **정상**: 18.5 ≤ BMI < 23
        - **과체중**: 23 ≤ BMI < 25
        - **비만**: BMI ≥ 25
        """)
        
    except ValueError as e:
        st.error(f"❌ 입력 오류: {str(e)}")
    except TypeError as e:
        st.error(f"❌ 타입 오류: {str(e)}")
    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>BMI 계산기 v1.0</div>",
    unsafe_allow_html=True
)
