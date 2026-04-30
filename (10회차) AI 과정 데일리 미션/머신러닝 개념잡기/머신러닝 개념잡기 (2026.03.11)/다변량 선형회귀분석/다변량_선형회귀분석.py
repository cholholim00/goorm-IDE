# 단변량 예제보다 조금 더 복잡한, 3개의 입력값(특징)을 가진 데이터를 학습
# 1. 환경 설정 및 데이터 준비
# 행렬 연산을 위해 데이터를 리스트가 아닌 행렬 형태로 구성합니다.
import torch
import torch.optim as optim

# 1-1. 다변량 데이터 생성 (입력 특성이 3개인 경우)
# x1, x2, x3가 각각 독립 변수입니다.
x_train = torch.FloatTensor([[73, 80, 75], 
                             [93, 88, 93], 
                             [89, 91, 90], 
                             [96, 98, 100], 
                             [73, 66, 70]])
y_train = torch.FloatTensor([[152], [185], [180], [196], [142]])
# Line-by-Line: 각 행은 하나의 데이터 샘플을 의미하며, x_train은 (5, 3) 크기의 행렬이 됩니다. 
# 5개의 샘플에 각각 3개의 특징이 있는 구조입니다.

# 2. 가중치(W)와 편향(b) 초기화
# 입력 특징이 3개이므로, 가중치 W도 3개가 필요합니다.

# 1-2. 모델 파라미터 초기화 (입력 차원에 맞춰 W의 크기를 3으로 설정)
W = torch.zeros((3, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)
# Line-by-Line: W를 (3, 1) 크기로 선언하여 행렬 곱셈(matmul)이 가능하게 합니다. 
# 초기값은 0이며 학습을 통해 최적값을 찾아갑니다.

# 3. 학습 설정 및 루프 진행
# 행렬 곱을 활용해 가설을 세우고 오차를 계산합니다.

# 1-3. 최적화 도구 설정 (경사하강법 사용)
optimizer = optim.SGD([W, b], lr=1e-5)
nb_epochs = 2000
for epoch in range(nb_epochs + 1):
    
    # 1-4. 가설 계산 (H(X) = XW + b) -> 행렬 곱셈 활용
    hypothesis = x_train.matmul(W) + b
    
    # 1-5. 비용 함수(MSE) 계산
    cost = torch.mean((hypothesis - y_train) ** 2)

    # 1-6. 오차 역전파 및 업데이트
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()
# Line-by-Line: matmul(W)은 여러 특징들을 한 번에 계산하는 효율적인 행렬 연산입니다. 
# lr=1e-5처럼 아주 작은 학습률을 사용한 이유는 데이터의 수치가 크기 때문에 학습이 발산하는 것을 막기 위함입니다.

    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} | Cost: {cost.item():.6f}')

# 4. 최종 학습 결과 확인
print("-" * 30)
print("학습 완료!")
print(f'최종 가중치 W:\n{W.detach()}')
print(f'최종 편향 b: {b.detach().item():.6f}')

# 5. 새로운 데이터로 예측 테스트 (반드시 3개의 특징을 넣어야 함)
# 예: [73, 80, 75] 데이터를 넣었을 때 정답 152에 가깝게 나오는지 확인
test_data = torch.FloatTensor([[73, 80, 75]])
prediction = test_data.matmul(W) + b

print("-" * 30)
print(f'입력값 [73, 80, 75]에 대한 예측값: {prediction.item():.2f} (실제 정답: 152)')

# 핵심 개념 포인트
# 행렬 연산의 효율성: 독립 변수가 많아져도 matmul을 통해 수식을 간결하게 유지할 수 있습니다.
# 가중치의 의미: 학습이 끝나면 각 W값의 크기를 통해 어떤 독립 변수가 결과값(y)에 더 큰 영향을 미치는지 파악할 수 있습니다.
# 데이터 스케일링: 위 예제처럼 데이터 수치가 크면 학습률(lr) 설정에 매우 민감해집니다. 실제 프로젝트에서는 데이터를 0과 1 사이로 정규화하는 과정이 추가되기도 합니다.
