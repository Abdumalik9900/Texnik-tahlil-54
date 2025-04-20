import yfinance as yf
import ta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_API_TOKEN = "TELEGRAM_API_TOKEN"

# Texnik tahlil funktsiyasi
def swing_trade_analysis(symbol):
    data = yf.download(symbol, period="7d", interval="1h")

    if data.empty or len(data) < 50:
        return f"{symbol} uchun yetarli ma'lumot yo'q."

    close = data['Close']

    # 'ta' kutubxonasi yordamida SMA hisoblash
    sma_20 = close.rolling(window=20).mean()
    sma_50 = close.rolling(window=50).mean()

    if sma_20.iloc[-1] > sma_50.iloc[-1]:
        return f"{symbol} uchun 🟢 **Sotib olish signali**: SMA 20 > SMA 50"
    elif sma_20.iloc[-1] < sma_50.iloc[-1]:
        return f"{symbol} uchun 🔴 **Sotish signali**: SMA 20 < SMA 50"
    else:
        return f"{symbol} uchun neytral signal."

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Aksiya tahlili uchun simbol kiriting. Masalan: /analyze NVDA")

# /analyze komandasi
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].upper()
        result = swing_trade_analysis(symbol)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Iltimos, aksiyaning simbolini kiriting, masalan: /analyze NVDA")

# Asosiy ishga tushirish
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))

    app.run_polling()

if __name__ == '__main__':
    main()
