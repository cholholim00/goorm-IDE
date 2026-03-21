import torch

# 1. 데이터 정의 (평수, 방 개수, 연식 등 수치 단위가 크게 다른 상황 가정)
x_train = torch.FloatTensor([[2000, 3, 15], 
                             [1500, 2, 10], 
                             [3500, 4, 30], 
                             [2500, 3, 20]])

# 2. 평균(mu)과 표준편차(sigma) 계산
# dim=0은 열(feature) 단위로 계산하라는 의미입니다.
mu = x_train.mean(dim=0)
sigma = x_train.std(dim=0)

# 3. Standardization 적용 (Z-score)
# (데이터 - 평균) / 표준편차
x_scaled = (x_train - mu) / sigma

print("Original Data:\n", x_train)
print("Scaled Data:\n", x_scaled)

# Line-by-Line:
# mu = x_train.mean(dim=0): 각 특성별(열별) 평균을 구합니다. (예: 평수의 평균, 방 개수의 평균 등)
# sigma = x_train.std(dim=0): 각 특성별 표준편차를 구하여 데이터가 퍼진 정도를 확인합니다.
# x_scaled = (x_train - mu) / sigma: 브로드캐스팅(Broadcasting) 기능을 통해 모든 데이터 샘플에 대해 표준화를 수행합니다. 이제 모든 특성은 0 근처의 비슷한 범위를 갖게 됩니다.