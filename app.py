import streamlit as st
from part4_generate_portfolio_features import generate_feature_df
from part5a_rule_based_recommender import rule_based_scoring
from part5b_visualize_portfolio import (
    plot_portfolio_pie,
    plot_sentiment_scores,
    plot_rsi,
    plot_return_vs_volatility,
    plot_price_trend
)

top_n = 3  # ✅ Add this



# Title
st.set_page_config(page_title="AI Stock Portfolio Recommender", layout="wide")
st.title("📈 AI Stock Portfolio Recommender")
st.markdown("Get portfolio suggestions using sentiment, technical indicators, and rule-based scoring.")

# Input
api_key = st.text_input("🔑 Enter your NewsAPI key:", type="password")
tickers_input = st.text_input("📥 Enter stock tickers (comma-separated):", value="AAPL, MSFT, GOOGL, TSLA, AMZN")

# Submit button
if st.button("📊 Generate Portfolio"):
    if not api_key or not tickers_input:
        st.warning("Please enter both API key and stock tickers.")
    else:
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

        with st.spinner("Fetching data and generating features..."):
            df = generate_feature_df(tickers, api_key)
            ranked = rule_based_scoring(df)

        st.success("✅ Portfolio Generated!")

        # Show ranked table
        st.subheader("📋 Ranked Portfolio")
        st.dataframe(ranked[["ticker", "score"]].round(4))

        # Show pie chart
        st.subheader("🥧 Allocation Chart")
        plot_portfolio_pie(ranked, top_n=3)

        st.markdown("### 📉 RSI Distribution")
        plot_rsi(ranked)

        st.markdown("### 🧠 Sentiment Comparison")
        plot_sentiment_scores(ranked)

        st.markdown("### 📊 Return vs Volatility")
        plot_return_vs_volatility(ranked)

        st.markdown("### 📈 Individual Price Trends")
        for ticker in ranked.head(top_n)["ticker"]:
            plot_price_trend(ticker)
