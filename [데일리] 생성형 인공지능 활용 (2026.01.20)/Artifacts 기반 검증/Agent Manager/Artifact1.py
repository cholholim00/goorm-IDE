import math
from typing import List, Optional

class HealthAnalyzer:
    """체질량 및 건강 데이터를 분석하는 클래스입니다."""
    
    # 매직 넘버를 상수로 정의하여 유지보수성 향상
    OVERWEIGHT_THRESHOLD = 25.0
    UNDERWEIGHT_THRESHOLD = 18.5

    def __init__(self, data: Optional[List[float]] = None):
        self.data = data if data else []

    def add_value(self, value: float) -> None:
        """데이터를 추가합니다."""
        self.data.append(value)

    def calculate_mean(self) -> float:
        """평균을 계산합니다. 데이터가 없으면 0.0을 반환합니다."""
        if not self.data:
            return 0.0
        return sum(self.data) / len(self.data)

    def calculate_variance(self) -> float:
        """분산을 계산합니다."""
        mean = self.calculate_mean()
        if not self.data:
            return 0.0
        # 리스트 컴프리헨션(List Comprehension)을 사용하여 간결하게 작성
        return sum((x - mean) ** 2 for x in self.data) / len(self.data)

    def calculate_std_dev(self) -> float:
        """표준편차를 계산합니다."""
        return math.sqrt(self.calculate_variance())

    def determine_status(self) -> str:
        """평균 값에 따른 건강 상태를 반환합니다."""
        mean = self.calculate_mean()
        if mean == 0.0:
            return "NO DATA"
        
        if mean > self.OVERWEIGHT_THRESHOLD:
            return "WARNING (Overweight)"
        elif mean < self.UNDERWEIGHT_THRESHOLD:
            return "LOW (Underweight)"
        else:
            return "NORMAL"

# --- 실행부 (메인 로직과 클래스 분리) ---
if __name__ == "__main__":
    analyzer = HealthAnalyzer()
    print("--- Health Analyzer v2.0 (Refactored) ---")
    
    while True:
        user_input = input("Enter number (or 'q' to finish): ").strip()
        if user_input.lower() == 'q':
            break
        
        try:
            analyzer.add_value(float(user_input))
        except ValueError:
            print("❌ 잘못된 입력입니다. 숫자를 입력해주세요.")

    print(f"\n📊 분석 결과:")
    print(f"1. 평균 (Mean): {analyzer.calculate_mean():.2f}")
    print(f"2. 분산 (Variance): {analyzer.calculate_variance():.2f}")
    print(f"3. 표준편차 (Std Dev): {analyzer.calculate_std_dev():.2f}")
    print(f"4. 상태 (Status): {analyzer.determine_status()}")