x, y = map(int, input().split()) # 캐릭터의 현재 위치 좌표
N = int(input()) # 웅덩이(장애인)의 개수
# 웅덩이들의 좌표 리스트
px = []
py = []
for _ in range(N):
    xi, yi = map(int, input().split())
    px.append(xi)
    py.append(yi)

Q = int(input()) # 이동 명령의 횟수
C = input().split() # 이동 명령들이 담긴 리스트(U,D,L,R)

for i in range(Q):
    cmd = C[i]
    # 다음 위치 계산
    if cmd == 'U': # Up (y 증가)
        next_x = x
        next_y = y + 1
    elif cmd == 'D': # Down (y 감소)
        next_x = x
        next_y = y - 1
    elif cmd == 'L': # Left (x 감소)
        next_x = x - 1
        next_y = y
    else: # Right (x 증가)
        next_x = x + 1
        next_y = y

    # 다음 위치가 웅덩이 위치인지 확인
    valid = True
    for i in range(N):
        # N개의 모든 웅덩이를 하나씩 확인하며 좌표가 겹치는지 검사
        if px[i] == next_x and py[i] == next_y:
            valid = False # 웅덩이가 있다! 이동 불가 판정
            break

    # 다음 위치가 괜찮은 위치라면 이동
    if valid:
        x = next_x
        y = next_y

print(x, y)