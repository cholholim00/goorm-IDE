import sys
def main():
    N = int(sys.stdin.readline())
    MOD = 10**9 + 7
    if N == 1: print(0); return
    if N == 2: print(1); return
    a, b = 0, 1
    for _ in range(N-2):
        a, b = b, (a+b) % MOD
    print(b)
main()