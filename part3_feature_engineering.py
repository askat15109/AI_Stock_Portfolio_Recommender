import yfinance as yf
import pandas as pd
import numpy as np
from part2_news_sentiment import get_news_sentiment

def get_stock_features(ticker, api_key):
    # 1. Fetch historical data
    df = yf.download(ticker, start="2020-01-01", end="2024-12-31")
    df.dropna(inplace=True)

    # 2. Calculate RSI manually
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # 3. Calculate MACD manually
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 4. Calculate return and volatility
    df['Return_7d'] = df['Close'].pct_change(periods=7)
    df['Volatility_7d'] = df['Close'].pct_change().rolling(window=7).std()

    # 5. Get sentiment score (1 value for the ticker)
    sentiment_score = get_news_sentiment(ticker, api_key, limit=10, verbose=False)

    # 6. Add constant column for sentiment (same for all rows)
    df['Sentiment'] = sentiment_score

    # 7. Final cleaning
    df.dropna(inplace=True)
    df['Ticker'] = ticker

    # 8. Select latest row as final feature vector
    latest = df.iloc[-1][['Ticker', 'RSI', 'MACD', 'MACD_Signal', 'Sentiment', 'Return_7d', 'Volatility_7d']]
    return latest
if __name__ == "__main__":
    api_key = "5e2122fc348a4d549cdd8eb39ff27112"  # 🔁 Replace with your real key
    features = get_stock_features("AAPL", api_key)
    print("\n✅ Final Feature Vector:\n", features)
