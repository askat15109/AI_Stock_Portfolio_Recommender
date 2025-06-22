import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_news_sentiment(ticker, api_key, limit=10, verbose=False):
    """
    Fetch recent news articles for a stock ticker and return average sentiment score.
    
    Parameters:
    - ticker (str): Stock symbol (e.g., 'AAPL', 'TSLA')
    - api_key (str): Your NewsAPI key
    - limit (int): Number of news headlines to analyze
    - verbose (bool): If True, prints sentiment per headline
    
    Returns:
    - float: Average compound sentiment score (-1 to 1)
    """
    url = f"https://newsapi.org/v2/everything?q={ticker}&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching news for {ticker}: {response.status_code}")
        return 0.0

    articles = response.json().get("articles", [])
    if not articles:
        print(f"No news found for {ticker}")
        return 0.0

    analyzer = SentimentIntensityAnalyzer()
    total_score = 0
    count = 0

    for article in articles[:limit]:
        title = article.get('title', '')
        description = article.get('description', '')
        content = f"{title}. {description}"

        sentiment = analyzer.polarity_scores(content)
        score = sentiment['compound']  # value between -1 and 1
        total_score += score
        count += 1

        if verbose:
            tag = 'Positive' if score > 0.2 else 'Negative' if score < -0.2 else 'Neutral'
            print(f"[{tag}] ({score:.4f}): {title}")

    if count == 0:
        return 0.0

    avg_score = total_score / count
    return round(avg_score, 4)

# Optional test block
if __name__ == "__main__":
    # Replace with your actual NewsAPI key
    api_key = "5e2122fc348a4d549cdd8eb39ff27112"
    ticker = "AAPL"

    sentiment = get_news_sentiment(ticker, api_key, limit=10, verbose=True)
    print(f"\n📈 Average Sentiment Score for {ticker}: {sentiment}")
