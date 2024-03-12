from tech_news.database import db
from datetime import datetime


def date_format(date):
    try:
        date_converted = datetime.strptime(date, "%Y-%m-%d")
        return date_converted.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")


def search_by_title(title):
    try:
        query = db.news.find(
            {"title": {"$regex": title, "$options": "i"}},
            projection=["title", "url"],
        )

        return [(item["title"], item["url"]) for item in query]

    except Exception as error:
        raise error


def search_by_date(date):
    date_formated = date_format(date)

    try:
        query = db.news.find(
            {"timestamp": date_formated},
            projection=["title", "url"],
        )

        return [(item["title"], item["url"]) for item in query]
    except Exception as error:
        raise error


def search_by_category(category):
    try:
        query = db.news.find(
            {"category": {"$regex": category, "$options": "i"}},
            projection=["title", "url"],
        )

        return [(item["title"], item["url"]) for item in query]

    except Exception as error:
        raise error
