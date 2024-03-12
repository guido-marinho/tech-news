from tech_news.database import find_news
from collections import Counter


def top_5_categories():
    news = find_news()
    categories = sorted([item["category"] for item in news])
    counter = Counter(categories)
    most_common = counter.most_common(5)
    return [category for category, count in most_common]
