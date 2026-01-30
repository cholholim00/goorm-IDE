


# f-string - 문자열 앞에 f를 붙이고 변수를 중괄호 {} 안에 넣는다.
name = "Alice"
age = 30
greeting = f"Hello, my name is {name} and I am {age} years old."
print(greeting)  # Hello, my name is Alice and I am 30 years old.

# format() 메서드 - 문자열의 format() 메서드를 사용하여 변수를 삽입한다.
name = "Bob"
age = 25
greeting = "Hello, my name is {} and I am {} years old.".format(name, age)
print(greeting)  # Hello, my name is Bob and I am 25 years old.

# % 연산자 - %s, %d 등의 포맷 지정자를 사용하여 변수를 삽입한다.
name = "Charlie"
age = 35
greeting = "Hello, my name is %s and I am %d years old." % (name, age)
print(greeting)  # Hello, my name is Charlie and I am 35 years old.

# 정렬 및 폭 지정
name = "David"
age = 28
greeting = f"Hello, my name is {name:<10} and I am {age:>5} years old."
print(greeting)  # Hello, my name is David      and I am    28 years old.

# 소수점 자리수 지정
pi = 3.141592653589793
formatted_pi = f"Pi rounded to 2 decimal places is {pi:.2f}"
print(formatted_pi)  # Pi rounded to 2 decimal places is 3.14

# 16진수, 8진수, 2진수 포맷팅
number = 255
hex_format = f"Hexadecimal: {number:#x}"
oct_format = f"Octal: {number:#o}"
bin_format = f"Binary: {number:#b}"
print(hex_format)  # 16진수: 0xff
print(oct_format)  # 8진수: 0o377
print(bin_format)  # 이진수: 0b11111111

# 퍼센트 포맷팅
percentage = 0.756
formatted_percentage = f"Percentage: {percentage:.2%}"
print(formatted_percentage)  # Percentage: 75.60%