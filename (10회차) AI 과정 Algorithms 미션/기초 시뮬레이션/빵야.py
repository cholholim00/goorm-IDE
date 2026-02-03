N = int(input())
H = list(map(int, input().split()))

ans = 0 # 정답
ct = 0 # 권총이 발사된 횟수

for i in range(N):

    # 권총이 주는 피해가 1이 될 때까지 그리고 적의 체력이 남아있는 동안 권총을 발사한다.
    while ct and H[i] > 0:
        H[i] -= ct + 1
        ct = (ct + 1) % 4
        ans += 1

    # 적이 쓰러졌다면 넘어간다.
    if H[i] <= 0:
        continue

    # 1,2,3,4 총 네 번의 발사가 반복되는 것을 한 번에 계산한다.
    q, H[i] = divmod(H[i], 10)
    ans += q * 4

    # 적이 쓰러지지 않았다면 체력은 10 미만이므로, 적의 체력이 남아있는 동안 권총을 발사한다.
    while H[i] > 0:
        H[i] -= ct + 1
        ct = (ct + 1) % 4
        ans += 1

print(ans)