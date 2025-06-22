import pandas as pd

def rule_based_scoring(df: pd.DataFrame):
    # 🧼 Normalize all column names to lowercase, remove spaces/underscores
    df.rename(columns=lambda col: col.strip().replace(" ", "_").replace("__", "_").lower(), inplace=True)

    # 🧾 Debug actual column names
    print("📋 Cleaned Columns:", df.columns.tolist())

    # ✅ Compute macd flag and score
    df["macd_signal_flag"] = (df["macd"] > df["macd_signal"]).astype(int)

    df["score"] = (
        0.4 * df["sentiment"] +
        0.3 * df["return_7d"] -
        0.2 * df["volatility_7d"] +
        0.1 * df["macd_signal_flag"]
    )

    ranked_df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return ranked_df







from part4_generate_portfolio_features import generate_feature_df
from part5a_rule_based_recommender import rule_based_scoring

api_key = "5e2122fc348a4d549cdd8eb39ff27112"
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

df = generate_feature_df(tickers, api_key)
ranked = rule_based_scoring(df)

print("\n📊 Final Ranked Portfolio:\n")
print(ranked[['ticker', 'score']])


