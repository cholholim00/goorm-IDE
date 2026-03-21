# 1. 환경 설정 및 데이터 준비공부 시간(x)에 따른 합격 여부(y, 0 또는 1) 데이터를 생성합니다.
import torch 
import torch.optim as optim

# 1-1. 데이터 생성 (x: 공부시간, y: 합격 1 / 불합격 0)
x_train = torch.FloatTensor([[1], [2], [3], [4], [5], [6]])
y_train = torch.FloatTensor([[0], [0], [0], [1], [1], [1]])
# Line-by-Line: 1~3시간 공부하면 불합격, 4~6시간 공부하면 합격하는 데이터셋입니다.

# 2. 로지스틱 회귀 모델 정의
# 분류를 위해 출력을 0과 1 사이로 압축하는 Sigmoid 함수를 사용합니다.
# 1-2. 모델 파라미터 초기화
W = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 1-3. 최적화 설정
optimizer = optim.SGD([W, b], lr=1) # 분류에서는 lr을 조금 크게 잡기도 합니다.

# 3. 학습 루프 및 비용 함수(BCELoss)
# 분류 문제에서는 MSE 대신 Binary Cross Entropy(BCE) 손실 함수를 사용합니다.
nb_epochs = 1000
for epoch in range(nb_epochs + 1):
    
    # 1-4. 가설 계산 (Sigmoid 적용)
    # H(x) = 1 / (1 + exp(-(Wx + b)))
    hypothesis = torch.sigmoid(x_train * W + b)
    
    # 1-5. 비용 함수 계산 (이진 교차 엔트로피)
    cost = -(y_train * torch.log(hypothesis) + (1 - y_train) * torch.log(1 - hypothesis)).mean()

    # 1-6. 업데이트
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} | Cost: {cost.item():.6f}')
# Line-by-Line: torch.sigmoid는 어떤 값이든 0~1 사이의 확률값으로 변환합니다. 
# cost 수식은 예측이 틀릴수록 값이 무한대로 커지도록 설계되어 모델이 정답을 강하게 쫓도록 만듭니다.

# 4. 결정 경계 확인 및 예측
# 학습된 모델이 0.5를 기준으로 어떻게 분류하는지 확인합니다.
# 1-7. 학습된 모델로 예측 (0.5보다 크면 1, 아니면 0)
prediction = hypothesis >= torch.FloatTensor([0.5])
print("-" * 30)
print(f'실제 정답:\n{y_train.detach()}')
print(f'모델의 예측:\n{prediction.float().detach()}')

# 1-8. 결정 경계(Decision Boundary) 계산
# Wx + b = 0 이 되는 지점이 확률 0.5인 경계선입니다.
boundary = -b.item() / W.item()
print(f'결정 경계(공부 시간 기준): {boundary:.2f}시간')
# Line-by-Line: hypothesis >= 0.5를 통해 최종 클래스를 결정합니다. 
# 계산된 boundary가 약 3.5라면, 모델은 "3.5시간 이상 공부하면 합격"이라는 선을 그은 셈입니다.