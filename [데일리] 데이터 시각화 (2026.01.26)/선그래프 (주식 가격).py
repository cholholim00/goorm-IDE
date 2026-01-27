import yfinance as yf
import matplotlib.pyplot as plt

# 삼성전자 주가 데이터 가져오기
data = yf.download('005930.KS', start='2023-01-01', end='2024-01-01')

plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Samsung Electronics')
plt.title('Stock Price Trend')
plt.xlabel('Date')
plt.ylabel('Price (KRW)')
plt.legend()
plt.grid(True)
plt.show()