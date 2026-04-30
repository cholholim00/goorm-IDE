import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup # [핵심] 분석가 등장

# --- [설정] ---
TARGET_URL = "https://product.kyobobook.co.kr/bestseller/total?saleCmdtDvsnCode=TOT&dsplDvsnCode=001"
FILE_NAME = "kyobo_bs4_result.csv"
# -------------

print("🚀 [1단계] Selenium: 사이트 접속 및 데이터 로딩")

# 1. Selenium 설정 (운반책)
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get(TARGET_URL)

    # 2. 데이터 로딩 대기 & 스크롤 (Selenium의 역할은 여기까지!)
    print("⏳ 데이터 로딩 대기 (7초)...")
    time.sleep(7)

    print("📜 스크롤 다운...")
    driver.execute_script("window.scrollTo(0, 2000);")
    time.sleep(3)

    # 3. [핵심] 운전기사(Selenium)가 분석가(BS4)에게 서류(HTML)를 넘깁니다.
    print("📄 [2단계] HTML 소스코드 추출 및 BS4 이양")
    html = driver.page_source

    # ---------------------------------------------------------
    # 여기서부터는 Selenium이 아니라 BeautifulSoup이 일합니다. (훨씬 빠름)
    # ---------------------------------------------------------

    print("🕵️ [3단계] BeautifulSoup: 링크 정밀 분석")
    soup = BeautifulSoup(html, 'html.parser')

    # CSS Selector 문법은 Selenium과 거의 똑같습니다.
    # a 태그 중에서 href 속성에 '/detail/'이 포함된 녀석들 찾기
    links = soup.select("a[href*='/detail/']")

    print(f"🎯 발견된 후보 링크: {len(links)}개")

    book_data = []
    seen_titles = set()

    for link in links:
        # BS4에서는 .text 대신 .get_text(strip=True)를 주로 씁니다.
        title = link.get_text(strip=True)
        # 속성 가져오기: Selenium은 .get_attribute('href'), BS4는 ['href']
        href = link['href']

        # [유효성 검사 로직은 동일]
        if title and len(title) > 2 and title not in seen_titles:
            if "장바구니" in title or "바로가기" in title:
                continue

            seen_titles.add(title)
            rank = len(seen_titles)

            print(f"{rank}위 | {title[:20]}...")
            book_data.append([rank, title, href])

            if len(book_data) >= 20: break

    # 4. 저장
    if len(book_data) > 0:
        with open(FILE_NAME, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["순위", "제목", "링크주소"])
            writer.writerows(book_data)
        print(f"\n🎉 [4단계] 저장 완료! '{FILE_NAME}' 생성됨.")
    else:
        print("\n❌ 수집 실패.")

except Exception as e:
    print(f"⚠️ 에러 발생: {e}")

finally:
    driver.quit()