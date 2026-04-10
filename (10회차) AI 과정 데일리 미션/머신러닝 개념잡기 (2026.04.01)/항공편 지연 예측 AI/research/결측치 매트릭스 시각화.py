import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

# 1. 데이터 로드 (시각화 파일에서도 데이터를 읽어야 'train'이 정의됩니다)
print("🚀 시각화를 위해 데이터를 로딩 중입니다...")
try:
    # 100만 건이라 로딩에 시간이 좀 걸립니다.
    train = pd.read_csv('dataset/train.csv')

    # 2. 결측치 매트릭스 시각화
    print("📊 결측치 매트릭스 생성 중... (창이 뜨면 확인 후 닫아주세요)")
    
    # 전체적인 결측치 패턴 (하얀 줄이 빈 곳입니다)
    msno.matrix(train)
    plt.title("Flight Delay Data Missing Matrix", fontsize=20)
    plt.show()

    # 결측치 간의 상관관계 (어떤 값이 비었을 때 다른 값도 비는지 확인)
    print("🔗 결측치 상관관계 히트맵 생성 중...")
    msno.heatmap(train)
    plt.show()

    # 3. 수치 요약
    print("\n" + "="*50)
    print("🎯 컬럼별 결측치 합계:")
    print(train.isnull().sum().sort_values(ascending=False))
    print("="*50)

except FileNotFoundError:
    print("❌ 파일을 찾을 수 없습니다. 'dataset/train.csv' 경로를 확인해주세요.")
except Exception as e:
    print(f"❌ 에러 발생: {e}")