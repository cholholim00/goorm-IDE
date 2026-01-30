# 조건문 
# if: 만약 ~라면
# elif: 그게 아니고 만약 ~라면 (여러 개 사용 가능)
# else: 위의 조건들이 모두 아니라면 (마지막 정리)

score = 85
if score >= 90:
    print("A학점")
elif score >= 80:
    print("B학점")
elif score >= 70:
    print("C학점")
else:
    print("F학점 : 재수강")
    
# 중첩 조건문
num = 15
if num % 2 == 0:
    if num % 3 == 0:
        print("2와 3의 공배수")
    else:
        print("2의 배수")
else:
    if num % 3 == 0:
        print("3의 배수")
    else:
        print("2와 3의 배수가 아님")
        
# 논리 연산자와 함께 사용
age = 25
has_license = True
if age >= 18 and has_license:
    print("운전 가능")
else:
    print("운전 불가")
    