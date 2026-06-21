import sys

def solve_string_split():
    # 입력 받기
    input = sys.stdin.read
    lines = input().split()
    if not lines:
        return
    
    N = int(lines[0])
    S = lines[1]
    
    combinations = []
    all_substrings = set()
    
    # 1. 3개의 부분 문자열로 나누는 모든 경우의 수 찾기
    # i, j는 나누는 경계선 인덱스
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            sub1 = S[:i]
            sub2 = S[i:j]
            sub3 = S[j:]
            
            combinations.append((sub1, sub2, sub3))
            all_substrings.add(sub1)
            all_substrings.add(sub2)
            all_substrings.add(sub3)
            
    # 2. 중복 제거 후 사전순 정렬하여 P 만들기
    P = sorted(list(all_substrings))
    
    # 각 부분 문자열의 점수를 빠르게 찾기 위해 딕셔너리(해시 맵) 활용
    # 인덱스는 1등부터 시작하므로 idx + 1
    word_to_score = {word: idx + 1 for idx, word in enumerate(P)}
    
    # 3. 최대 점수 계산
    max_score = 0
    for sub1, sub2, sub3 in combinations:
        current_score = word_to_score[sub1] + word_to_score[sub2] + word_to_score[sub3]
        if current_score > max_score:
            max_score = current_score
            
    print(max_score)

if __name__ == "__main__":
    solve_string_split()