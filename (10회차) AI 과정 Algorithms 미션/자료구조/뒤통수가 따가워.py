import sys
input = sys.stdin.readline

N = int(input())
h = list(map(int, input().split()))

stk = [] # 스택
for i in range(N): # 첫 번째 신선부터 확인해본다.
	# i번째 신선을 보는 신선들은 곧 스택에 남아 있는 신선들이다.
	print(len(stk), end = ' ')

	# 스택에 남아 있는 신선들에 대해, 봉우리의 높이가 반드시 감소하는 꼴이 되게 해야 한다.
	# 봉우리의 높이가 h_i보다 같거나 낮은 모든 신선들을 스택에서 pop해야 한다.
	while stk and h[stk[-1]] <= h[i]:
		stk.pop()

	# 스택에 i번째 신선을 넣었을 때
	# 스택에 남아 있는 신선들의 봉우리 높이는 반드시 감소하는 꼴을 이루고 있다.
	stk.append(i)