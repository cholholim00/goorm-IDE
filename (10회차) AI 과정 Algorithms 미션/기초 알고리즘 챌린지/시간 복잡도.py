N = int(input())

# N!을 소인수분해했을 때의 5의 개수를 세어줘야 한다.
ct = 0
while N:
    N //= 5
    ct += N

print(ct)