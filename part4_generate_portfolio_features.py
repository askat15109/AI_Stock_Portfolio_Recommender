from part3_feature_engineering import get_stock_features
import pandas as pd

def generate_feature_df(tickers, api_key):
    """
    Generates a DataFrame of feature vectors for a list of tickers.
    """
    all_features = []

    for ticker in tickers:
        try:
            print(f"\n🔍 Processing {ticker}...")
            features = get_stock_features(ticker, api_key)
            if features is not None:
                all_features.append(features)
            else:
                print(f"⚠️ Skipped {ticker}: No data returned.")
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")

    if not all_features:
        print("⚠️ No features collected. Exiting.")
        return pd.DataFrame()

    # Combine all into a DataFrame
    feature_df = pd.DataFrame(all_features)
    return feature_df.reset_index(drop=True)

if __name__ == "__main__":
    api_key = "5e2122fc348a4d549cdd8eb39ff27112"
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

    df = generate_feature_df(tickers, api_key)
    print("\n✅ Final Feature DataFrame:\n")
    print(df)
