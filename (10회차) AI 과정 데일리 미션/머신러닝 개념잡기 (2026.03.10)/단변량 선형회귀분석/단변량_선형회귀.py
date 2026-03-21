# 데이터 생성부터 모델 훈련까지의 전 과정을 단계별 실습
## 1. 환경 설정 및 데이터 준비
# 먼저 학습에 필요한 라이브러리를 불러오고, 시뮬레이션용 데이터를 생성합니다.
import torch
import torch.optim as optim

# 1-1. 학습 데이터 생성 (x가 입력, y가 정답 데이터)
x_train = torch.FloatTensor([[1], [2], [3]])
y_train = torch.FloatTensor([[2], [4], [6]])

# Line-by-Line: 'torch' 라이브러리를 통해 텐서 연산을 준비합니다. 
# x가 1, 2, 3일 때 y가 2, 4, 6이 되는 간단한 선형 관계(2배)를 설정했습니다.

## 2. 가중치($w$)와 편향($b$) 초기화
# 모델이 학습하며 업데이트할 변수를 정의합니다.

# 1-2. 모델 파라미터 초기화 (0으로 시작, 학습 가능하도록 설정)
W = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
# Line-by-Line: 'requires_grad=True' 를 설정해야 PyTorch가 해당 변수에 대한 미분(Gradient)을 계산하여 자동으로 학습을 진행합니다.

## 3. 가설 설정 및 손실 함수 정의
# 모델의 예측 식과 실제 값과의 차이를 계산하는 기준을 정합니다.

# 1-3. 최적화 도구 설정 (경사하강법 사용, 학습률 0.01)
optimizer = optim.SGD([W, b], lr=0.01)

# 1-4. 학습 루프 (1000번 반복)
nb_epochs = 1000
for epoch in range(nb_epochs + 1):
    # 가설(Hypothesis) 계산: y = Wx + b
    hypothesis = x_train * W + b
    # 비용 함수(Cost function): 평균 제곱 오차(MSE) 계산
    cost = torch.mean((hypothesis - y_train) ** 2)
# Line-by-Line: `SGD`는 확률적 경사 하강법으로, 모델의 오차를 줄이기 위해 W와 b를 조금씩 수정합니다. 
# `cost`는 예측값과 실제값의 차이를 제곱하여 평균낸 값으로, 이 값이 0에 가까워지는 것이 목표입니다.

## 4. 경사 하강법 수행 (Gradient Descent)
# 오차를 바탕으로 가중치를 업데이트합니다.

    # 1-5. 오차를 역전파하여 파라미터 업데이트
    optimizer.zero_grad() # 기울기 초기화
    cost.backward()       # 비용 함수 미분하여 기울기 계산
    optimizer.step()      # 파라미터 업데이트
# Line-by-Line: `zero_grad()`는 이전 단계의 기울기가 남지 않도록 비워주는 과정입니다. 
# `backward()`는 수식적으로 미분을 수행하는 핵심 단계이며, `step()`을 통해 비로소 W와 b가 수정됩니다.

# 100번마다 학습 상태 출력
    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} | Cost: {cost.item():.6f}')

## 1-6
# 임의의 데이터로 예측값 확인
# 변수 이름이 정확히 'new_input'인지 확인하세요!
new_input = torch.FloatTensor([[5]]) 

# 예측 계산
prediction = new_input * W + b

print("-" * 30)
print(f'x가 5일 때 모델의 예측 y값: {prediction.item():.2f}')