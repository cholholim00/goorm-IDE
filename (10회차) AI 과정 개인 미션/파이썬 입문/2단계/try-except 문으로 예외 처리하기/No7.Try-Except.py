# 예외 처리
# 구조:
# try: 에러가 날 가능성이 있는 코드를 넣습니다.
# except: 에러가 났을 때 실행할 '대안' 코드를 넣습니다.
text = "백만원"

try:
    # 숫자로 바꿀수 없는 문자열을 int()로 변환 시도
    number = int(text)
    print(f"변환 성공: {number}")
    
except ValueError:
    # ValueError 예외가 발생했을 때 실행할 코드
    print(f"변환 실패: '{text}'는(은) 숫자가 아닙니다.")
    
print("프로그램 종료")

# 실전 코드 연습

print("=== 안전한 나눗셈 계산기 (종료하려면 'EXIT' 입력) ===")

while True:
    1. # 사용자로부터 입력 받기
    user_input = input("나눗셈 계산기 > ")
    
    2. # 'EXIT' 입력 시 프로그램 종료
    if user_input.upper() == "EXIT":
        print("프로그램을 종료합니다.")
        break
    
    try:
        # 3. 예외가 발생할 수 있는 작업 (변환 및 나눗셈)
        dividend = int(user_input) # 입력을 정수로 변환
        divisor = 2               # 2로 나누기
        
        result = dividend / divisor
        print(f"결과: {dividend} / {divisor} = {result}")
        
    except ValueError:
        # 4. ValueError 예외 처리
        print("오류: 유효한 정수를 입력하세요.")
        
    except ZeroDivisionError:
        # 5. ZeroDivisionError 예외 처리 (이 경우는 발생하지 않지만 예시로 포함)
        print("오류: 0으로 나눌 수 없습니다.")
        
    except Exception as e:
        # 6. 기타 모든 예외 처리
        print(f"알 수 없는 오류가 발생했습니다: {e}")