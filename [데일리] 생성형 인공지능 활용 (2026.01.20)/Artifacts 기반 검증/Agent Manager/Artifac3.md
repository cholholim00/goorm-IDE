# 🏥 Health Data Analyzer

## 개요
환자 또는 사용자의 수치 데이터를 입력받아 기초 통계(평균, 분산, 표준편차)를 분석하고
건강 위험도(BMI 등)를 분류하는 Python 모듈입니다.

## 주요 기능
- **안전한 계산**: 데이터가 없어도 프로그램이 멈추지 않도록 예외 처리
- **상태 분류**: 
  - `WARNING`: 25.0 초과
  - `NORMAL`: 18.5 ~ 25.0
  - `LOW`: 18.5 미만

## 사용 방법 (Example)
```python
from health_analyzer import HealthAnalyzer

analyzer = HealthAnalyzer([22.5, 23.0, 21.8])
print(analyzer.determine_status()) # Output: NORMAL