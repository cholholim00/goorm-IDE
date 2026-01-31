from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 텍스트 데이터
text = "데이터 분석 파이썬 시각화 워드클라우드 시각화 파이썬"

# 2. 맥용 폰트 경로 설정 (이 부분이 핵심입니다)
# 시스템에 따라 경로가 다를 수 있으니 아래 두 가지 중 하나를 선택하세요.
font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'

# 3. 워드클라우드 생성
# font_path를 설정하지 않으면 기본 폰트(DroidSans)를 찾으려다 에러가 날 수 있습니다.
wc = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=400
).generate(text)

# 4. 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()