
import yfinance as yf
from telegram import Bot
import time
import asyncio

TOKEN = "8123102770:AAG_h6qiVxSJmNYxSQIUnaQRIQO2MxiRfgE"
CHAT_ID = '6124148024'  # /start bosgan odamning ID'si

bot = Bot(token=TOKEN)

async def check_stock():
    while True:
        # Aksiya tanlang (masalan: Apple - AAPL)
        ticker = yf.Ticker("AAPL")
        df = ticker.history(period="14d")

        close = df['Close']
        sma = close.rolling(window=10).mean()
        rsi = 100 - (100 / (1 + (close.pct_change().dropna().mean() / close.pct_change().dropna().std())))

        signal = ""

        if close[-1] > sma[-1] and rsi < 70:
            signal = "📈 Ko‘tarilish signali: AAPL narxi 10 kunlik SMA dan yuqori."
        elif close[-1] < sma[-1] and rsi > 30:
            signal = "📉 Tushish signali: AAPL narxi 10 kunlik SMA dan past."

        if signal:
            await bot.send_message(chat_id=CHAT_ID, text=signal)

        await asyncio.sleep(3600)  # 1 soatda bir marta tekshir

asyncio.run(check_stock())
