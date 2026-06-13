import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 페이지 설정 ---
st.set_page_config(page_title="논문 실습 마스터", layout="wide")

st.title("👨‍💻 논문 실습 마스터: Paper to Code")
st.markdown("논문을 업로드하면 **데이터셋 링크**와 **단계별 실행 코드**를 생성해줍니다.")

# --- 사이드바: 설정 ---
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Google Gemini API Key", type="password")
    st.markdown("[API Key 발급받기](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    st.markdown("### 💡 사용 팁")
    st.info("1. API 키를 입력하세요.\n2. PDF를 업로드하세요.\n3. '실습 가이드 생성' 버튼을 누르세요.")

# --- 메인 기능 ---
uploaded_file = st.file_uploader("PDF 논문을 업로드하세요", type="pdf")

if uploaded_file is not None:
    # 1. 텍스트 추출
    reader = PdfReader(uploaded_file)
    paper_text = ""
    for page in reader.pages:
        paper_text += page.extract_text()
    
    st.success(f"논문 분석 준비 완료! ({len(reader.pages)} 페이지)")

    # 2. 버튼 클릭 시 분석 시작
    if st.button("🚀 실습 가이드 & 코드 생성"):
        if not api_key:
            st.error("먼저 왼쪽 사이드바에 API Key를 입력해주세요!")
        else:
            try:
                genai.configure(api_key=api_key)
                # 성능이 좋은 Gemini 2.5 Flash 모델 사용
                model = genai.GenerativeModel('gemini-2.5-flash')

                # --- 3. 강력해진 프롬프트 (여기가 핵심!) ---
                prompt = f"""
                당신은 시니어 AI 엔지니어입니다. 이 논문을 읽고 주니어 개발자가 당장 내일부터 실습할 수 있도록 구체적인 튜토리얼을 작성해주세요.
                추상적인 설명은 피하고, **실행 가능한 코드**와 **구체적인 링크**를 제공해야 합니다.

                ---
                ### 1. 데이터셋 준비 (Dataset Preparation)
                * 이 논문에서 사용한 데이터셋 이름은 무엇인가요?
                * **다운로드 링크:** (Kaggle, HuggingFace, PapersWithCode 등 실제 다운로드 가능한 URL을 제공하세요. 만약 비공개 데이터라면 가장 유사한 공개 데이터셋 링크를 주세요.)
                * **데이터 구조:** 데이터가 폴더별로 정리되어야 하는지 등 디렉토리 구조를 설명하세요.

                ### 2. 환경 설정 (Prerequisites)
                * 필요한 라이브러리 설치 명령어 (`pip install ...`)

                ### 3. 단계별 구현 (Step-by-Step Implementation)
                각 단계별로 바로 복사해서 실행할 수 있는 Python 코드를 작성하세요. (주로 PyTorch 또는 TensorFlow 사용)

                **Step 1: 데이터 로더 (Data Loader)**
                * 데이터를 불러오고 전처리하는 코드

                **Step 2: 모델 아키텍처 (Model Architecture)**
                * 논문의 핵심 모델을 Class 형태로 구현한 코드

                **Step 3: 학습 루프 (Training Loop)**
                * Loss Function, Optimizer 설정 및 학습을 진행하는 코드

                ### 4. 핵심 하이퍼파라미터
                * 논문에서 추천하는 Learning Rate, Batch Size, Epoch 수 등을 표로 정리하세요.
                ---

                [논문 텍스트]:
                {paper_text}
                """

                # 4. 결과 생성 및 출력
                with st.spinner("논문을 분석하고 실행 코드를 작성 중입니다... (약 30초 소요)"):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")