# 공식: lambda 입력변수: 결과값
# 일반 함수로 만들때
def plus_ten(x):
    return x + 10

# 람다 함수로 만들때
plus_ten_lambda = lambda x: x + 10
print(plus_ten(5))          # 출력: 15
print(plus_ten_lambda(5))   # 출력: 15

# 여러 개의 입력 변수를 가지는 람다 함수
multiply = lambda x, y: x * y
print(multiply(3, 4))      # 출력: 12

# 람다 함수를 다른 함수의 인자로 전달하기
def apply_function(func, value):
    return func(value)
result = apply_function(lambda x: x ** 2, 6)
print(result)               # 출력: 36

# 리스트의 각 요소에 람다 함수 적용하기
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x ** 2, numbers))
print(squared_numbers)      # 출력: [1, 4, 9, 16, 25]

# 필터링에 람다 함수 사용하기
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)         # 출력: [2, 4]

# 정렬에 람다 함수 사용하기
points = [(1, 2), (3, 1), (5, 4), (2, 3)]
points.sort(key=lambda point: point[1])
print(points)              # 출력: [(3, 1), (1, 2), (2, 3), (5, 4)]

# 람다 함수로 간단한 조건문 작성하기
max_value = lambda a, b: a if a > b else b
print(max_value(10, 20))   # 출력: 20

# 중첩된 람다 함수
nested_lambda = lambda x: (lambda y: x + y)
add_five = nested_lambda(5)
print(add_five(10))        # 출력: 15

# 람다 함수와 리스트 컴프리헨션 결합하기
incremented_numbers = [(lambda x: x + 1)(num) for num in numbers]
print(incremented_numbers)  # 출력: [2, 3, 4, 5, 6]

