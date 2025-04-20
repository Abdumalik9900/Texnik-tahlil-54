
import yfinance as yf
import talib as ta
import pandas as pd
import numpy as np
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TELEGRAM_API_TOKEN = "8123102770:AAG_h6qiVxSJmNYxSQIUnaQRIQO2MxiRfgE"
# Swing trade botning funksiyasi
def swing_trade_analysis(symbol):
    # Aksiya ma'lumotlarini olish
    data = yf.download(symbol, period="7d", interval="1h")  # 7 kunlik ma'lumotlar, har 1 soatda yangilanadi

    # Yopilish narxlarini olish
    close = data['Close']

    # Simple Moving Average (SMA) hisoblash
    sma_20 = ta.SMA(close, timeperiod=20)
    sma_50 = ta.SMA(close, timeperiod=50)

    # Signalni aniqlash
    if sma_20[-1] > sma_50[-1]:
        return f"{symbol} uchun sotib olish signal: SMA 20 > SMA 50"
    elif sma_20[-1] < sma_50[-1]:
        return f"{symbol} uchun sotish signal: SMA 20 < SMA 50"
    else:
        return f"{symbol} uchun signal yo'q."

# Telegram xabarini yuborish
def start(update, context):
    update.message.reply_text("Salom! Aksiya tahlili uchun `symbol`ni kiriting. Masalan, `NVDA`.")

def analyze(update, context):
    if context.args:
        symbol = context.args[0]
        result = swing_trade_analysis(symbol)
        update.message.reply_text(result)
    else:
        update.message.reply_text("Iltimos, aksiyaning simbolini kiriting, masalan: `/analyze NVDA`.")

# Telegram botni sozlash
def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Start komandasi
    dispatcher.add_handler(CommandHandler('start', start))

    # Analyze komandasi
    dispatcher.add_handler(CommandHandler('analyze', analyze))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
