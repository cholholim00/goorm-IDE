import pytest
from Artifact1 import HealthAnalyzer

def test_initialization():
    """초기화 테스트"""
    analyzer = HealthAnalyzer()
    assert analyzer.data == []

def test_calculate_mean():
    """평균 계산 로직 검증"""
    analyzer = HealthAnalyzer([23.5, 25.1, 19.8])
    assert analyzer.calculate_mean() == 22.8

def test_empty_data_safety():
    """데이터가 비어있을 때 0으로 나누는 에러가 발생하지 않는지 검증"""
    analyzer = HealthAnalyzer([])
    # 0으로 나누기 에러 대신 0.0이 반환되어야 함
    assert analyzer.calculate_mean() == 0.0
    assert analyzer.calculate_variance() == 0.0

def test_status_warning():
    """과체중 경고 로직 테스트"""
    analyzer = HealthAnalyzer([30.0, 30.0]) # 평균 30
    assert "WARNING" in analyzer.determine_status()

if __name__ == "__main__":
    # 1. 만든 테스트 함수들을 하나씩 직접 실행시킵니다.
    try:
        test_initialization()
        print("✅ 초기화 테스트 통과!")
        
        test_calculate_mean()
        print("✅ 평균 계산 테스트 통과!")
        
        test_empty_data_safety()
        print("✅ 빈 데이터 안전장치 테스트 통과!")
        
        test_status_warning()
        print("✅ 경고 문구 테스트 통과!")
        
        print("\n🎉 모든 테스트가 성공적으로 끝났습니다!")
        
    except AssertionError:
        print("\n❌ 테스트 실패! 어딘가 값이 다릅니다.")
    except Exception as e:
        print(f"\n⚠️ 에러 발생: {e}")