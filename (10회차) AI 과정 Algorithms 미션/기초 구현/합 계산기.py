result = 0
T = int(input())

for i in range(T):
    s = input().split()
    firstNum = int(s[0])
    command = s[1]
    secondNum = int(s[2])
    
    if command == "+":
        result += firstNum + secondNum
    elif command == "-":
        result += firstNum - secondNum
    elif command == "*":
        result += firstNum * secondNum
    else:
        result += firstNum // secondNum

print(result)
