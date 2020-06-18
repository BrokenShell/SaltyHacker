from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


sid_obj = SentimentIntensityAnalyzer()


def sentiment_score(sentence: str) -> int:
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return int(-sentiment_dict['compound'] * 10000)
