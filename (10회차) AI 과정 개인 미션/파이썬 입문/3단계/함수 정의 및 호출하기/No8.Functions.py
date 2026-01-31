# 함수 정의하기
def greet(name, age):
    massage = f"안녕하세요, {name}님! 당신은 {age}살입니다."
    return massage # return 키워드를 사용하여 값을 반환합니다.

# 함수 호출하기
result = greet("철수", 25)
print(result)  # 출력: 안녕하세요, 철수님! 당신은 25살살입니다.

# 여러 값을 반환하는 함수
def calculate_area_and_perimeter(width, height):
    area = width * height
    perimeter = 2 * (width + height)
    return area, perimeter  # 튜플 형태로 여러 값을 반환합니다.

# 함수 호출하기
area, perimeter = calculate_area_and_perimeter(5, 10)
print(f"면적: {area}, 둘레: {perimeter}")  # 출력 : 면적: 50, 둘레: 30

# 반환값이 없는 함수
def print_welcome_message():
    print("환영합니다! 이 함수는 반환값이 없습니다.")
    
# 간단한 계산기 함수 정의하기
def add_numbers(a, b):
    return a + b

sum_result = add_numbers(3, 7)
print(f"덧셈 결과: {sum_result}")  # 출력: 덧셈 결과: 10

def subtract_numbers(a, b):
    return a - b

subtraction_result = subtract_numbers(10, 4)
print(f"뺄셈 결과: {subtraction_result}")  # 출력: 뺄셈 결과: 6

def multiply_numbers(a, b):
    return a * b

product_result = multiply_numbers(4, 5)
print(f"곱셈 결과: {product_result}")  # 출력: 곱셈 결과: 20

def divide_numbers(a, b):
    if b == 0:
        return "0으로 나눌 수 없습니다."
    return a / b

division_result = divide_numbers(10, 2)
print(f"나눗셈 결과: {division_result}")  # 출력: 나눗셈 결과: 5.0



