# 1. 환경 설정 및 비선형 데이터 생성실제 정답이 $y = 3x^2 + 2x + 1$인 데이터를 만들어봅니다. - Pythonimport torch
import torch
import torch.optim as optim

# 1-1. 비선형 데이터 생성
x_train = torch.FloatTensor([[1], [2], [3], [4]])
# 정답: 3x^2 + 2x + 1 에 약간의 노이즈를 가정
y_train = torch.FloatTensor([[6], [17], [34], [57]])
# Line-by-Line: x_train은 (4, 1) 형태이며, 이에 대응하는 곡선 형태의 정답 y_train을 설정했습니다.

# 2. 다항 특징(Polynomial Features) 생성
# 입력 데이터 x를 [x, x^2] 형태의 행렬로 변환합니다.

# 1-2. x^2 항을 추가하여 다항 데이터 행렬 생성 [x, x^2]
x_poly = torch.cat([x_train, x_train**2], dim=1) 
# 결과: [[1, 1], [2, 4], [3, 9], [4, 16]]
# Line-by-Line: torch.cat을 사용하여 기존 x값 옆에 x의 제곱값을 붙입니다. 이제 모델은 두 개의 특징을 가진 다변량 회귀처럼 동작하게 됩니다.

# 3. 모델 파라미터 및 학습 설정
# 특징이 2개(x, x^2)이므로 가중치 $W$도 2개가 필요합니다.

# 1-3. 모델 파라미터 초기화 (W는 2개, b는 1개)
W = torch.zeros((2, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 4. 최적화 도구 설정
optimizer = optim.SGD([W, b], lr=0.001)
# Line-by-Line: W의 크기를 (2, 1)로 설정하여 행렬 곱셈이 가능하게 합니다. 학습률은 수치가 커지는 것을 고려해 적절히 조절합니다.

# 1-4. 학습 루프 진행
# 비용 함수를 최소화하며 곡선의 파라미터를 찾아갑니다.
nb_epochs = 5000
for epoch in range(nb_epochs + 1):
    
    # 5. 가설 계산 (H(X) = XW + b) -> 여기서 X는 [x, x^2]
    hypothesis = x_poly.matmul(W) + b
    
    # 6. 비용 함수(MSE) 계산 및 업데이트
    cost = torch.mean((hypothesis - y_train) ** 2)
    
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()
# Line-by-Line: x_poly.matmul(W)를 수행하면 내부적으로 $w_1x + w_2x^2 + b$가 계산됩니다. 이는 결국 곡선 형태의 예측값을 만들어냅니다.

# [추가] 200번마다 학습 상태 출력
    if epoch % 200 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} | Cost: {cost.item():.6f}')

# 6. 최종 학습 결과 확인
print("-" * 30)
print("학습 완료!")
# W[0]은 x의 계수(2), W[1]은 x^2의 계수(3)에 가까워집니다.
print(f'최종 가중치 W (x, x^2):\n{W.detach()}')
print(f'최종 편향 b: {b.detach().item():.6f}')

# 7. 새로운 데이터로 곡선 예측 테스트
# x=5일 때, 정답은 3(25) + 2(5) + 1 = 86 입니다.
test_x = torch.FloatTensor([[5]])
test_x_poly = torch.cat([test_x, test_x**2], dim=1) # 테스트 데이터도 똑같이 변환!
prediction = test_x_poly.matmul(W) + b

print("-" * 30)
print(f'x가 5일 때 모델의 예측값: {prediction.item():.2f} (실제 정답: 86.00)')