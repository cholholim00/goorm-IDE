# 1. 환경 설정 및 초기값 설정
# 우리가 찾고자 하는 정답이 y=2x인 상황을 가정합니다.
import torch

# 1-1. 데이터 설정
x_train = torch.FloatTensor([[1], [2], [3]])
y_train = torch.FloatTensor([[2], [4], [6]])

# 1-2. 가중치 W를 임의의 값(5.0)으로 초기화 (원래 정답은 2)
W = torch.tensor([5.0], requires_grad=True)
# Line-by-Line: W를 정답인 2와 거리가 먼 5로 설정했습니다. 
# requires_grad=True를 통해 이 변수의 기울기를 추적할 수 있도록 합니다.

# 2. 가설 및 손실 함수 정의
# 현재의 W값이 얼마나 틀렸는지 계산합니다.
# 1-3. 학습률(Learning Rate) 설정
lr = 0.1

print("--- 학습 시작 ---")
# 1-4. 학습 루프 (10번만 진행하며 변화 확인)
for step in range(11):
    # 가설 계산
    hypothesis = x_train * W
    # 비용 함수(MSE) 계산
    cost = torch.mean((hypothesis - y_train) ** 2)
# Line-by-Line: lr은 한 번에 얼마나 멀리 이동할지를 결정하는 보폭입니다. 
# cost는 예측값과 실제값의 차이를 제곱하여 평균낸 것으로, 이 값이 작아질수록 정답에 가까워집니다.

# 3. 경사 계산 및 업데이트 (핵심 단계)
# 미분을 통해 기울기를 구하고 W를 수정합니다.

    # 1-5. 기울기 계산 (미분)
    optimizer_zero_grad = W.grad # 이전 기울기가 있다면 비워줘야 함 (수동 구현 시)
    if W.grad is not None:
        W.grad.zero_()
        
    cost.backward() # 비용 함수를 W로 미분하여 기울기(Gradient) 도출
    
    # 1-6. W 업데이트: W = W - (lr * 기울기)
    with torch.no_grad(): # 파라미터 업데이트 시에는 기록을 남기지 않음
        W -= lr * W.grad

    # 1번마다 현재 상태 출력
    print(f'Step {step:2d} | W: {W.item():.4f} | Gradient: {W.grad.item():7.4f} | Cost: {cost.item():.4f}')
# Line-by-Line: cost.backward()를 호출하면 W에 대한 기울기가 W.grad에 저장됩니다. 
# 이후 W에서 (학습률 × 기울기)만큼을 빼서 새로운 W를 만듭니다. 기울기가 양수면 왼쪽으로, 음수면 오른쪽으로 이동하게 됩니다.
    print("--- 학습 종료 ---")
    print(f'최종 학습 결과: W = {W.item():.4f} (정답 2.0에 수렴)')