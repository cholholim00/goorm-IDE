import streamlit as st
import shap
import xgboost
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="아파트 가격 분석기", page_icon="🏢")

st.title("🏢 서울 아파트 가격은 무엇이 결정할까?")
st.markdown("""
AI가 아파트 가격을 예측하고, **왜 그 가격으로 예측했는지(SHAP)** 설명해줍니다.
데이터는 이해를 돕기 위해 생성한 가상의 데이터입니다.
""")

# ---------------------------------------------------------
# 1. 한국형 가상 데이터 생성 (Korean Synthetic Data)
# ---------------------------------------------------------
@st.cache_data
def make_korean_housing_data():
    np.random.seed(42)
    N = 1000
    
    # 1. 변수 생성 (영어 변수명 사용 - 그래프 폰트 깨짐 방지)
    data = {
        'Size_Pyung': np.random.randint(20, 60, N),       # 평수 (20~60평)
        'Station_Dist': np.random.randint(1, 20, N),      # 역까지 거리 (분)
        'Year_Built': np.random.randint(1990, 2024, N),   # 건축 연도
        'Is_Gangnam': np.random.randint(0, 2, N),         # 강남 여부 (0:비강남, 1:강남)
        'Parking': np.random.uniform(0.5, 2.5, N)         # 세대당 주차대수
    }
    df = pd.DataFrame(data)
    
    # 2. 가격(Target) 계산 로직 (현실 반영)
    # 기본 5억 + 평당 3천 + 강남이면 10억 추가 - 역에서 멀수록 감소 + 신축 프리미엄
    base_price = 50000 
    price = (
        base_price +
        (df['Size_Pyung'] * 3000) +           # 평수 클수록 비쌈
        (df['Is_Gangnam'] * 100000) -         # 강남이면 10억 뜀
        (df['Station_Dist'] * 1000) +         # 역에서 멀면 쌈
        ((df['Year_Built'] - 1990) * 500)     # 신축일수록 비쌈
    )
    # 약간의 랜덤 노이즈 추가
    price += np.random.normal(0, 5000, N)
    
    return df, price

# 데이터 로드
X, y = make_korean_housing_data()

# 데이터 미리보기
with st.expander("📊 학습 데이터 미리보기 (상위 5개)"):
    st.write("변수 설명: `Size_Pyung`(평수), `Station_Dist`(역보도시간), `Is_Gangnam`(강남여부)")
    st.dataframe(X.head())

# ---------------------------------------------------------
# 2. 모델 학습 (XGBoost)
# ---------------------------------------------------------
model = xgboost.XGBRegressor().fit(X, y)

# ---------------------------------------------------------
# 3. SHAP 값 계산 (AI의 생각 읽기)
# ---------------------------------------------------------
explainer = shap.TreeExplainer(model)
shap_values = explainer(X)

# ---------------------------------------------------------
# 4. 시각화 (Streamlit SHAP)
# ---------------------------------------------------------
from streamlit_shap import st_shap

st.divider()

# (1) 전체 요인 분석
st.header("1. 무엇이 집값에 가장 큰 영향을 줄까요?")
st.info("💡 **그래프 보는 법:** 점이 **오른쪽(양수)**에 있으면 집값을 올리는 요인, **왼쪽(음수)**이면 집값을 깎는 요인입니다.")

st_shap(shap.plots.beeswarm(shap_values), height=300)

st.markdown("""
**🔍 분석 결과:**
* **Is_Gangnam (강남여부):** 빨간 점(1=강남)이 오른쪽에 몰려있죠? 강남이면 집값이 확 뜁니다.
* **Size_Pyung (평수):** 빨간 점(큰 평수)일수록 오른쪽에 있습니다. 평수가 클수록 비쌉니다.
* **Station_Dist (역 거리):** 빨간 점(거리가 멂)이 왼쪽에 있습니다. 역세권이 아닐수록 집값이 떨어집니다.
""")

st.divider()

# (2) 개별 아파트 분석
st.header("2. 특정 아파트 가격 분석 (Waterfall)")
st.write("첫 번째 아파트가 왜 이 가격으로 예측되었는지 분석합니다.")

# 첫 번째 데이터 뽑기
sample_idx = 0
prediction = model.predict(X.iloc[[sample_idx]])[0]

st.metric(label="예측된 아파트 가격", value=f"{prediction/10000:.1f} 억원")

st_shap(shap.plots.waterfall(shap_values[sample_idx]), height=300)

st.markdown("""
**🔍 상세 분석:**
* 그래프의 **밑바닥(E[f(x)])**은 서울 아파트 평균 가격입니다.
* 여기서 **빨간 막대**는 가격을 올린 이유(예: 강남이라서, 평수가 커서),
* **파란 막대**는 가격을 깎은 이유(예: 역에서 멀어서)입니다.
* 다 합치면 **최종 예측 가격(f(x))**이 됩니다.
""")