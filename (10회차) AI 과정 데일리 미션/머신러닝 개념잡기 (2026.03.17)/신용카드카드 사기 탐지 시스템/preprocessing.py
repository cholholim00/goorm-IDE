# preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import config

def load_and_preprocess():
    # 1. 데이터 로드
    df = pd.read_csv(config.DATA_PATH)
    
    # 2. 피처 엔지니어링 (Step 2 내용 반영)
    # 시간(Time)을 24시간 단위의 'Hour'로 변환
    df['Hour'] = (df['Time'] // 3600) % 24
    
    # 금액(Amount) 로그 변환 (치우친 분포 완화)
    df['Log_Amount'] = np.log1p(df['Amount'])
    
    # 3. 스케일링 (V1~V28과 보조를 맞춤)
    scaler = StandardScaler()
    df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
    
    # 4. 불필요한 원본 컬럼 제거
    df.drop(['Time', 'Amount'], axis=1, inplace=True)
    
    print("✅ 데이터 전처리 및 피처 생성 완료")
    return df

if __name__ == "__main__":
    df = load_and_preprocess()
    print(df[['Hour', 'Log_Amount', 'Class']].head())