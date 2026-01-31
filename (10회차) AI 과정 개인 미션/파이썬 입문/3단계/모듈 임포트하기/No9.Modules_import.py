# 수학 모듈 전체 불러오기
import math
print("math 모듈 전체 불러오기")
print("원주율 (pi):", math.pi)
print("자연로그 밑 (e):", math.e)
print("3의 제곱근:", math.sqrt(3))
print("5의 팩토리얼:", math.factorial(5))

# 수학 모듈에서 특정 함수만 불러오기
from math import pow, log
print("\nmath 모듈에서 특정 함수만 불러오기")
print("2의 3제곱:", pow(2, 3))
print("e의 자연로그:", log(math.e))

# 수학 모듈의 함수에 별칭 붙이기
import random as rd
print("\nmath 모듈의 함수에 별칭 붙이기")
print(rd.random(1, 10)) # 1부터 10 사이의 임의의 실수 생성
print(rd.choice(['짜장', '짬뽕', '탕수육'])) # 리스트에서 임의의 요소 선택

# 수학 모듈의 모든 함수와 변수를 불러오기
from math import *
print("\nmath 모듈의 모든 함수와 변수를 불러오기")
print("사인 30도:", sin(30))
print("코사인 60도:", cos(60))
print("탄젠트 45도:", tan(45))
print("로그 1000:", log10(1000))
print("자연로그 20:", log(20))
print("5의 제곱근:", sqrt(5))
print("원주율 (pi):", pi)
print("자연로그 밑 (e):", e)
print("5의 팩토리얼:", factorial(5))
print("3의 제곱근:", sqrt(3))
print("2의 8제곱:", pow(2, 8))
print("올림값:", ceil(4.2))
print("내림값:", floor(4.8))
print("절댓값:", fabs(-7.5))
print("삼각함수 아크사인 (0.5):", asin(0.5))
print("삼각함수 아크코사인 (0.5):", acos(0.5))
print("삼각함수 아크탄젠트 (1):", atan(1))
print("하이퍼볼릭 사인 (1):", sinh(1))
print("하이퍼볼릭 코사인 (1):", cosh(1))
print("하이퍼볼릭 탄젠트 (1):", tanh(1))
print("각도(radian) 변환 (90도):", radians(90))
print("각도(degree) 변환 (π/2):", degrees(pi/2))
print("로그 감마 함수 (5):", lgamma(5))
print("감마 함수 (5):", gamma(5))
print("모듈러 곱셈 역원 (3, 11):", modf(3.75))
print("유클리드 호제법 (48, 18):", gcd(48, 18))
print("조합 (5, 2):", comb(5, 2))
print("순열 (5, 2):", perm(5, 2))
print("하이퍼볼릭 아크사인 (1):", asinh(1))
print("하이퍼볼릭 아크코사인 (1):", acosh(1))
print("하이퍼볼릭 아크탄젠트 (0.5):", atanh(0.5))
