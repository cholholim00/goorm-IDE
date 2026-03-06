import pandas as pd

def run_final_integration_fixed():
    # 1. 모든 데이터 로드
    artist = pd.read_csv('dataset/아티스트_앨범_트랙/애플뮤직_아티스트.csv')
    album = pd.read_csv('dataset/아티스트_앨범_트랙/애플뮤직_앨범.csv')
    track = pd.read_csv('dataset/아티스트_앨범_트랙/애플뮤직_트랙.csv')
    
    user_subs = pd.read_csv('dataset/appleMusic_회원_및_구독_데이터/user_subscriptions.csv')
    plans = pd.read_csv('dataset/appleMusic_회원_및_구독_데이터/subscription_plans.csv')
    
    users = pd.read_csv('dataset/플레이리스트&로그분석/users.csv')
    playlist = pd.read_csv('dataset/플레이리스트&로그분석/playlist.csv')
    playlist_track = pd.read_csv('dataset/플레이리스트&로그분석/playlist_track.csv')

    print("✅ 데이터 로드 완료. ID 정규화를 시작합니다.")

    # --- 2. ID 불일치 해결 (전처리 리더의 핵심 작업) ---
    
    # [정규화 1] 유저 ID 맞추기: U001 -> US001 로 변환
    user_subs['user_id'] = user_subs['user_id'].str.replace('U', 'US', regex=False)
    
    # [정규화 2] 트랙 ID 맞추기: TR001 -> T001 로 변환
    playlist_track['track_id'] = playlist_track['track_id'].str.replace('TR', 'T', regex=False)

    # --- 3. 데이터 통합 (Merge) ---

    # [A] 음악 마스터 생성
    music_master = pd.merge(track, album, on='album_id', how='left')
    music_master = pd.merge(music_master, artist, on='artist_id', how='left', suffixes=('', '_art'))

    # [B] 유저 및 구독 마스터 생성
    user_master = pd.merge(users, user_subs, on='user_id', how='left')
    user_master = pd.merge(user_master, plans, on='plan_id', how='left')

    # [C] 최종 로그 통합 (모든 정보 결합)
    final_log = pd.merge(playlist_track, playlist[['playlist_id', 'user_id', 'playlist_name']], on='playlist_id', how='left')
    final_log = pd.merge(final_log, music_master, on='track_id', how='left')
    final_log = pd.merge(final_log, user_master, on='user_id', how='left', suffixes=('', '_user_info'))

    # --- 4. 최종 저장 ---
    final_log.to_csv('dataset/APPLE_MUSIC_TOTAL_MASTER.csv', index=False, encoding='utf-8-sig')
    
    print("\n" + "="*40)
    print("🚀 통합 완료 리포트 (수정본)")
    print(f"- 최종 통합 행 수: {len(final_log)}건")
    print(f"- 연결된 고유 아티스트: {final_log['artist_name'].nunique()}명 (연결 성공!)")
    print("- 결과 파일: dataset/APPLE_MUSIC_TOTAL_MASTER.csv")
    print("="*40)

# 실행
run_final_integration_fixed()