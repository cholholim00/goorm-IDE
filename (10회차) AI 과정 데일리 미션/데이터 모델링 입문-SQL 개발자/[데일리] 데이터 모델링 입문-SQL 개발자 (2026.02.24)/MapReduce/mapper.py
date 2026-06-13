import sys

# 표준 입력(stdin)에서 데이터를 한 줄씩 읽어옵니다.
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # 데이터를 쉼표(,) 기준으로 분리합니다.
    parts = line.split(',')
    if len(parts) != 3:
        continue
    
    user_id, song_id, play_time = parts
    
    # 1. 결측치 제거: 곡 ID가 없는 경우 건너뜀
    if not song_id:
        continue
    
    # 2. 이상한 값 처리: 재생 시간이 숫자가 아니거나 0 이하인 오류 로그 건너뜀
    try:
        play_time = int(play_time)
        if play_time <= 0:
            continue
    except ValueError:
        continue
        
    # 전처리를 통과한 정상 데이터만 Key(song_id)와 Value(1) 형태로 출력
    # 탭(\t) 문자로 Key와 Value를 구분합니다.
    print(f"{song_id}\t1")