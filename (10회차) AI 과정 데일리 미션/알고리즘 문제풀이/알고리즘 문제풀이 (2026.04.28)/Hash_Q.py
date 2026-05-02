## 문제1번
# 문자열의 가장 먼저 나오는 유일한 문자 찾기
def first_unique_char(s):
    count = {}
    # 빈도수 계산
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    # 앞에서부터 유일한 문자 찾기
    for i in range(len(s)):
        if count[s[i]] == 1:
            return i
    return -1
# 예시: "loveleetcode" -> 2 ('v')

# 문제2번
# 합이 0인 부분 배열 중 가장 긴 것 찾기
def largest_subarray_zero_sum(arr):
    hash_map = {}
    max_len = 0
    curr_sum = 0
    
    for i in range(len(arr)):
        curr_sum += arr[i]
        
        if curr_sum == 0:
            max_len = i + 1
        
        if curr_sum in hash_map:
            max_len = max(max_len, i - hash_map[curr_sum])
        else:
            hash_map[curr_sum] = i
            
    return max_len
# 예시: [15, -2, 2, -8, 1, 7, 10, 23] -> 5

## 문제3번
# 영어 끝말잇기
def solution(n, words):
    used_words = set([words[0]])
    
    for i in range(1, len(words)):
        # 1. 이미 말한 단어이거나 2. 앞 단어와 이어지지 않을 때
        if words[i] in used_words or words[i-1][-1] != words[i][0]:
            player = (i % n) + 1
            turn = (i // n) + 1
            return [player, turn]
        
        used_words.add(words[i])
        
    return [0, 0]
# 예시: n=3, words=["tank", "kick", "know", "wheel", "land", "dream", "mother", "robot", "tank"] -> [3, 3]

if __name__ == "__main__":
    print("=== [문제 1] 유일한 문자 인덱스 ===")
    print(f"leetcode -> {first_unique_char('leetcode')}")
    print(f"loveleetcode -> {first_unique_char('loveleetcode')}")

    print("\n=== [문제 2] 합이 0인 가장 긴 부분 배열 길이 ===")
    A = [15, -2, 2, -8, 1, 7, 10, 23]
    print(f"배열 {A} -> 결과: {largest_subarray_zero_sum(A)}")

    print("\n=== [문제 3] 영어 끝말잇기 결과 ===")
    n, words = 3, ["tank", "kick", "know", "wheel", "land", "dream", "mother", "robot", "tank"]
    print(f"참가자 {n}명 결과 -> {solution(n, words)}")