# 소수 판정 O(root n)
def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1): #  n의 제곱근까지만 체크
        if not n % i:
            return False
    return True

N = int(input())
A = [int(input()) for _ in range(N)]

# 판타스틱한 갑옷은 결국 소수인 점수를 가지고 있어야 한다.
for i in range(N):
    if is_prime(A[i]):
        print('Yes')
    else:
        print('No')