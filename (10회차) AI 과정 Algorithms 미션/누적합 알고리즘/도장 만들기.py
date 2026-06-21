import sys

def solve():
    input = sys.stdin.readline
    
    # N: 문자열 S의 길이, S: 도장집 문자열
    N, S = input().split()
    N = int(N)
    
    # 알파벳 빈도수를 위한 2차원 누적 합 배열 생성
    # count_prefix[i][c] -> 1번째부터 i번째 글자까지 알파벳 c의 누적 등장 횟수
    # 알파벳 소문자 'a'의 아스키코드(97)를 기준으로 0~25 인덱스 사용
    count_prefix = [[0] * 26 for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        # 이전 누적 값 복사
        for c in range(26):
            count_prefix[i][c] = count_prefix[i - 1][c]
        # 현재 글자의 알파벳 카운트 증가
        current_char_idx = ord(S[i - 1]) - ord('a')
        count_prefix[i][current_char_idx] += 1
        
    # Q: 상황의 개수
    Q = int(input())
    
    output = []
    for _ in range(Q):
        # l, r: 구간, M: 문자열 T의 길이, T: 목표 문자열
        l_str, r_str, M_str, T = input().split()
        l, r, M = int(l_str), int(r_str), int(M_str)
        
        # 1. 목표 문자열 T에서 필요한 알파벳 글자 수 세기
        t_counts = {}
        for char in T:
            t_counts[char] = t_counts.get(char, 0) + 1
            
        # 2. 구간 [l, r] 내에서 사용 가능한 알파벳 개수를 구해 만들 수 있는 최대 개수 측정
        max_stamps = float('inf')
        
        for char, required_cnt in t_counts.items():
            char_idx = ord(char) - ord('a')
            # 구간 내 해당 알파벳의 총 개수 = prefix[r] - prefix[l-1]
            available_cnt = count_prefix[r][char_idx] - count_prefix[l - 1][char_idx]
            
            # 하나라도 필요한 글자가 부족하면 도장을 만들 수 없음
            if available_cnt < required_cnt:
                max_stamps = 0
                break
                
            # 해당 글자로 만들 수 있는 최대 몫 계산 후 최솟값 갱신
            max_stamps = min(max_stamps, available_cnt // required_cnt)
            
        output.append(str(max_stamps))
        
    print('\n'.join(output))

if __name__ == '__main__':
    solve()