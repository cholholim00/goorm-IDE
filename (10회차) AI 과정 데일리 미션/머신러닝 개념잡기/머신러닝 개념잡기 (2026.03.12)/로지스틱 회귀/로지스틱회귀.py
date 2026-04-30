# 1. 환경 설정 및 데이터 준비이진 분류를 위해 정답(y) 데이터를 0과 1로 구성합니다.
import torch.optim as optim
import torch.nn.functional as F
import torch

# 1-1. 데이터 생성 (x: 공부시간, y: 합격 1 / 불합격 0)
x_train = torch.FloatTensor([[1], [2], [3], [4], [5], [6]])
y_train = torch.FloatTensor([[0], [0], [0], [1], [1], [1]])
# Line-by-Line: x_train은 학습 데이터, y_train은 정답지입니다. 
# 3시간 이하면 0, 4시간 이상이면 1이 되도록 설정했습니다.

# 2. 모델 파라미터 및 최적화 설정기본적인 선형 회귀와 동일하게 W와 b를 초기화합니다.
# 1-2. 모델 파라미터 초기화
W = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 1-3. 최적화 도구 설정 (경사하강법 사용)
optimizer = optim.SGD([W, b], lr=1)

# 3. 학습 루프 및 시그모이드 적용
# 출력값을 확률로 바꾸고, 분류 전용 손실 함수인 Binary Cross Entropy를 사용합니다.
nb_epochs = 1000
for epoch in range(nb_epochs + 1):
    
    # 1-4. 가설 계산 (Sigmoid 적용: 0~1 사이 값으로 변환)
    # hypothesis = 1 / (1 + torch.exp(-(x_train.matmul(W) + b))) 와 동일
    hypothesis = torch.sigmoid(x_train * W + b)
    
    # 1-5. 비용 함수(Cost) 계산 (이진 교차 엔트로피)
    cost = F.binary_cross_entropy(hypothesis, y_train)

    # 1-6. 오차 역전파 및 업데이트
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    # 100번마다 진행 상황 출력
    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} | Cost: {cost.item():.6f}')
# Line-by-Line: torch.sigmoid는 직선의 결과를 곡선(S-자)으로 꺾어줍니다. 
# F.binary_cross_entropy는 예측값이 정답(0 또는 1)과 멀어질수록 아주 큰 벌점을 주는 함수입니다.

# 4. 최종 결과 확인 및 예측학습된 모델이 새로운 데이터를 어떻게 판단하는지 확인합니다.
# 1-7. 최종 파라미터 출력
print("-" * 30)
print(f'최종 가중치 W: {W.detach().item():.2f}')
print(f'최종 편향 b: {b.detach().item():.2f}')

# 1-8. 예측 테스트 (0.5를 기준으로 분류)
# x=3.5일 때 합격 확률 예측
test_x = torch.FloatTensor([[3.5]])
prob = torch.sigmoid(test_x * W + b)
prediction = prob >= 0.5 # 0.5 이상이면 True(1), 미만이면 False(0)

print("-" * 30)
print(f'x=3.5일 때 합격 확률: {prob.item()*100:.2f}%')
print(f'최종 예측 결과: {"합격(1)" if prediction else "불합격(0)"}')