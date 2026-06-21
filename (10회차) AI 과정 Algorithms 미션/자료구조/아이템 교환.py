import sys
input = sys.stdin.readline

N, M = map(int, input().split())

# 구름이가 갖고 있는 아이템을 셋에 담는다.
Goorm = set()
for item in input().split():
    Goorm.add(item)

# 친구가 갖고 있는 아이템을 셋에 담는다.
Friend = set()
for item in input().split():
    Friend.add(item)

for _ in range(M):
    a, b = input().split()

    # a를 구름이가 갖고 있고, b를 친구가 갖고 있으면 교환한다.
    if a in Goorm and b in Friend:

        # 구름이는 a를, 친구는 b를 잃는다.
        Goorm.remove(a)
        Friend.remove(b)

        # 구름이는 b를, 친구는 a를 얻는다.
        Goorm.add(b)
        Friend.add(a)

# 아이템의 이름을 사전순으로 출력하기 위해 정렬한다.
Goorm = sorted(Goorm)

for item in Goorm:
    print(item, end = ' ')