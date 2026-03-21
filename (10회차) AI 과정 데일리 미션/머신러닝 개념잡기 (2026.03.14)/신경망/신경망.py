# 1. 환경 설정 및 데이터 준비Pythonimport torch
import torch.nn as nn
import torch.optim as optim
import torch

# 1-1. 데이터 생성 (입력 2개, 출력 1개)
X = torch.FloatTensor([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = torch.FloatTensor([[0], [1], [1], [0]]) # XOR 문제 데이터
# Line-by-Line: torch.nn은 신경망 구조를 정의하는 도구들을 담고 있습니다. 
# XOR 데이터는 직선 하나로 나눌 수 없는 대표적인 비선형 문제입니다.

# 2. 신경망 모델 설계 (Architecture)
# 은닉층을 추가하여 모델이 복잡한 경계를 만들 수 있게 합니다.

# 1-2. 신경망 모델 정의 (입력2 -> 은닉층10 -> 출력1)
model = nn.Sequential(
    nn.Linear(2, 10), # 첫 번째 레이어: 입력 2개, 뉴런 10개
    nn.Sigmoid(),    # 활성화 함수: 비선형성 부여
    nn.Linear(10, 1), # 두 번째 레이어: 뉴런 10개, 출력 1개
    nn.Sigmoid()     # 최종 출력: 0~1 사이 확률값
)
# Line-by-Line: nn.Linear는 선형 변환(Wx + b)을 수행하고, nn.Sigmoid는 이를 꺾어서 비선형 패턴을 학습할 수 있게 합니다.
# 은닉층의 뉴런 개수(10개)는 사용자가 조절할 수 있는 하이퍼파라미터입니다.

# 3. 손실 함수 및 최적화 설정
# 1-3. 오차 계산법(BCE)과 최적화 알고리즘(Adam) 설정
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.1)
# Line-by-Line: 이진 분류이므로 BCELoss를 사용합니다. 
# Adam은 경사 하강법의 발전된 형태로, 학습 속도를 스스로 조절하여 훨씬 효율적으로 최적점을 찾습니다.

# 4. 학습 루프 (Forward & Backward)
# 1-4. 학습 시작
for epoch in range(1001):
    # Forward 연산: 모델에 데이터를 넣어 결과 계산
    hypothesis = model(X)
    # 오차(Cost) 계산
    cost = criterion(hypothesis, Y)
    # Backward 연산: 오차를 바탕으로 기울기 계산 및 업데이트
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    # 100번마다 결과 출력
    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/1000 | Cost: {cost.item():.6f}')
# Line-by-Line: model(X)를 호출하면 정의한 레이어들을 차례로 통과합니다. 
# backward()는 출력층에서 입력층 방향으로 오차를 전파하며 가중치를 수정하는데, 이를 역전파(Backpropagation)라고 부릅니다.

# 5. 최종 결과 확인 및 예측
# 학습이 끝난 모델이 XOR 문제를 해결했는지 확인합니다.
# 1-5. 예측값 확인
print("-" * 30)
with torch.no_grad():
    predicted = (model(X) > 0.5).float()
    accuracy = (predicted == Y).float().mean()
    print(f'모델의 예측값:\n{predicted.detach()}')
    print(f'실제 정답:\n{Y.detach()}')
    print(f'정확도: {accuracy.item() * 100}%')