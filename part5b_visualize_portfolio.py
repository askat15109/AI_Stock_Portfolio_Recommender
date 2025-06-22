import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import streamlit as st

# 🧠 1. Sentiment Comparison Bar Chart
def plot_sentiment_scores(df):
    fig, ax = plt.subplots()
    ax.bar(df["ticker"], df["sentiment"], color='orange')
    ax.set_title("🧠 Public Sentiment per Stock")
    ax.set_ylabel("Sentiment Score")
    ax.axhline(0, color='gray', linestyle='--')
    st.pyplot(fig)

# 📉 2. RSI Bar Chart
def plot_rsi(df):
    fig, ax = plt.subplots()
    ax.bar(df["ticker"], df["rsi"], color='skyblue')
    ax.axhline(70, color='red', linestyle='--', label='Overbought')
    ax.axhline(30, color='green', linestyle='--', label='Oversold')
    ax.set_title("📉 RSI (Relative Strength Index)")
    ax.set_ylabel("RSI")
    ax.legend()
    st.pyplot(fig)

# 📊 3. Return vs Volatility Scatter Plot
def plot_return_vs_volatility(df):
    fig, ax = plt.subplots()
    ax.scatter(df["volatility_7d"], df["return_7d"], c=df["score"], cmap="viridis", s=100)
    for i, row in df.iterrows():
        ax.text(row["volatility_7d"], row["return_7d"], row["ticker"])
    ax.set_xlabel("Volatility (7d)")
    ax.set_ylabel("Return (7d)")
    ax.set_title("📊 Return vs Volatility")
    ax.grid(True)
    st.pyplot(fig)

# 📈 4. Price Trend Line Chart
def plot_price_trend(ticker):
    data = yf.download(ticker, period="3mo")
    fig, ax = plt.subplots()
    ax.plot(data["Close"], label="Close Price")
    ax.set_title(f"{ticker} - Price Trend (Last 3 Months)")
    ax.set_ylabel("Price ($)")
    ax.grid(True)
    st.pyplot(fig)

def plot_portfolio_pie(ranked_df, top_n=3):
    top_picks = ranked_df.head(top_n).copy()
    total_score = top_picks["score"].sum()
    top_picks["weight"] = top_picks["score"] / total_score

    colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854"]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        top_picks["weight"],
        labels=top_picks["ticker"],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors[:top_n]
    )
    ax.set_title(f"📊 Recommended Portfolio Allocation (Top {top_n})")
    ax.axis('equal')
    st.pyplot(fig)


if __name__ == "__main__":
    import pandas as pd

    # Dummy data to test
    sample_data = {
        'ticker': ['GOOGL', 'AAPL', 'TSLA'],
        'score': [0.21, 0.20, 0.19]
    }
    ranked = pd.DataFrame(sample_data)



