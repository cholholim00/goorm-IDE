import sys

def solve():
    # 입력 처리
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N_cnt = int(line1[0])
        
        line2 = sys.stdin.readline().split()
        if not line2: return
        digits = sorted([int(x) for x in line2]) # 오름차순 정렬 필수
        
        line3 = sys.stdin.readline().strip()
        if not line3: return
        K_str = line3
        K_len = len(K_str)
        K_val = int(K_str)
    except ValueError:
        return

    min_val = digits[0] # 가장 작은 숫자

    candidates = []

    # Case 1: K보다 자릿수가 긴 경우 (즉, K가 3자리라면 4자리 중 가장 작은 수)
    # 가장 앞자리는 0이 아니어야 함 (문제 조건: 양의 정수는 0으로 시작 불가)
    # 하지만 0 < A_1이므로 digits에 0만 있는 경우는 없음 (N=1일때 A1!=0 조건)
    # 가능한 가장 작은 자릿수 늘리기 전략:
    # (0이 아닌 가장 작은 수) + (가장 작은 수) * (K길이)
    
    start_digit = -1
    for d in digits:
        if d != 0:
            start_digit = d
            break
            
    if start_digit != -1:
        # K 길이 + 1 만큼 가장 작은 수로 채움
        val_str = str(start_digit) + str(min_val) * K_len
        candidates.append(int(val_str))

    # Case 2: K와 자릿수가 같은 경우
    # K의 앞에서부터 i번째 자리까지는 K와 동일하게 가다가,
    # i번째 자리에서 K[i]보다 큰 숫자를 선택하고,
    # 그 뒤(i+1 ~ 끝)는 가장 작은 숫자로 채우는 방식
    
    for i in range(K_len):
        # i번째 자리(pivot)를 결정
        
        # 1. i번째 자리 이전까지는 K와 동일한 숫자를 만들 수 있어야 함
        # 즉, K의 0~i-1번째 숫자들이 모두 내 digits 목록에 있어야 함
        prefix = ""
        possible_prefix = True
        for j in range(i):
            if int(K_str[j]) not in digits:
                possible_prefix = False
                break
            prefix += K_str[j]
        
        if not possible_prefix:
            # 앞부분을 똑같이 못 만들면, 그 뒤의 pivot은 의미가 없음 (이미 더 앞에서 틀어졌으므로)
            # 하지만 Loop 구조상 여기서 break 하면 안됨. 
            # (예: K=123, digits={1,3}. i=1일때 '1'은 만들 수 있음. 
            # i=2일때 '1','2' 만들어야 하는데 '2'가 없어서 불가능. 즉 여기서 break가 맞음)
            break 
            
        # 2. i번째 자리에 K[i]보다 큰 숫자(d)를 넣음
        current_k_digit = int(K_str[i])
        for d in digits:
            if d > current_k_digit:
                # 찾았다! 
                # (앞부분 prefix) + (현재 큰 수 d) + (나머지는 최소값 min_val로 채움)
                suffix_len = K_len - 1 - i
                candidate_str = prefix + str(d) + str(min_val) * suffix_len
                candidates.append(int(candidate_str))
                # i번째 자리에서 d를 선택해서 이겼으므로, 더 큰 d를 볼 필요 없이 이 자리에서는 이게 최선임
                break 
    
    # 후보들 중 K보다 큰 수이면서 최솟값을 찾음
    # (로직상 생성된 모든 후보는 K보다 큼)
    if candidates:
        print(min(candidates))
    else:
        # 이론상 Case 1 때문에 비어있을 수 없음 (N>=1, A1!=0 이면 무조건 큰 수 생성 가능)
        pass

if __name__ == "__main__":
    solve()