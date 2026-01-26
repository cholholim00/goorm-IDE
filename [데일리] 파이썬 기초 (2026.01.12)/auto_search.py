import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

KEYWORD = input("검색어를 입력하세요 (예: 삼성전자): ")
print(f"🚀 [{KEYWORD}] 내용 기반 수집 로봇(최종) 가동!")

# 브라우저 열기
driver = webdriver.Chrome()
driver.maximize_window()

try:
    url = f"https://search.naver.com/search.naver?where=news&query={KEYWORD}"
    driver.get(url)

    print("⏳ 로딩 대기 중 (5초)...")
    time.sleep(5)

    # 1. 화면에 있는 모~든 링크(a 태그)를 다 긁어옵니다. (이름표 상관없음)
    print("🔎 모든 링크를 검사하는 중...")
    all_links = driver.find_elements(By.TAG_NAME, "a")

    news_data = []

    # 2. 하나씩 검사해서 우리 조건에 맞는 것만 골라냅니다.
    for link in all_links:
        try:
            text = link.text
            href = link.get_attribute("href")

            # [조건]
            # 1. 제목에 검색어가 포함되어 있어야 함
            # 2. 제목 길이가 10글자 이상이어야 함 (너무 짧은 메뉴 버튼 제외)
            # 3. 링크(href)가 있어야 함
            if text and href and (KEYWORD in text) and len(text) > 10:

                # 중복 저장 방지 (이미 담은 건지 확인)
                if [text, href] not in news_data:
                    news_data.append([text, href])
                    print(f"  - [발견] {text[:30]}...")

        except:
            continue # 에러 나면 다음 링크로 넘어감

    print(f"📊 최종 수집된 개수: {len(news_data)}개")

    # 3. 저장하기
    if len(news_data) > 0:
        file_name = f"{KEYWORD}_최종결과.csv"
        with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["제목", "링크"])
            writer.writerows(news_data)
        print(f"\n🎉 드디어 성공! '{file_name}' 파일을 확인해주세요.")
    else:
        print("\n❌ 0개입니다. (검색어가 포함된 긴 제목의 링크가 하나도 없습니다)")

except Exception as e:
    print(f"⚠️ 에러 발생: {e}")

finally:
    driver.quit()