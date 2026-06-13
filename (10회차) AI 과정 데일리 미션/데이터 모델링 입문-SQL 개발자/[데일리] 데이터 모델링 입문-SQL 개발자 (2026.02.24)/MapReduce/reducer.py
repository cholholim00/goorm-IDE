import sys

current_song = None
current_count = 0

# 표준 입력(stdin)에서 데이터를 한 줄씩 읽어옵니다.
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # 탭(\t)을 기준으로 Key(곡 ID)와 Value(카운트)를 분리합니다.
    song_id, count = line.split('\t', 1)
    
    try:
        count = int(count)
    except ValueError:
        continue
        
    # 동일한 곡 ID가 들어오면 카운트를 누적합니다.
    if current_song == song_id:
        current_count += count
    else:
        # 새로운 곡 ID가 나타나면, 이전 곡의 누적 결과를 출력합니다.
        if current_song:
            print(f"{current_song}\t{current_count}")
        
        # 새로운 곡 ID와 카운트로 초기화합니다.
        current_song = song_id
        current_count = count

# 마지막 곡의 결과를 출력합니다.
if current_song == song_id:
    print(f"{current_song}\t{current_count}")