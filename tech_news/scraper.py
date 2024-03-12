import requests
import time
from bs4 import BeautifulSoup
import re
from tech_news.database import create_news


def fetch(url):
    try:
        res = requests.get(
            url,
            headers={"user-agent": "Fake User Agent"},
            timeout=3,
        )

        time.sleep(1)

        if res.status_code != 200:
            return None

        return res.text
    except requests.RequestException:
        return None


def scrape_updates(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    links = []

    for a in soup.find_all("article", {"class": "entry-preview"}):
        link = a.find("a", href=True)["href"]
        links.append(link)

    return links


def scrape_next_page_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    try:
        next_page = soup.find("a", {"class": "next"}, href=True)["href"]
        return next_page
    except TypeError:
        return None


def scrape_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    category = soup.find("span", {"class": "label"}).text.strip()
    reading_time_text = soup.find("li", {"class": "meta-reading-time"}).text
    reading_time = int(re.search(r"\d+", reading_time_text).group())
    summary = soup.find("div", {"class": "entry-content"}).p.text.strip()
    title = soup.find("h1", {"class": "entry-title"}).text.strip()
    timestamp = soup.find("li", {"class": "meta-date"}).text
    url = soup.find("link", {"rel": "canonical"})["href"]
    writer = soup.find("span", {"class": "author"}).a.text

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


def get_tech_news(amount):
    data = []
    URL_BASE = "https://blog.betrybe.com/"

    while len(data) < amount:
        response = fetch(URL_BASE)
        links = scrape_updates(response)

        for link in links:
            news_content = fetch(link)
            news_data = scrape_news(news_content)
            data.append(news_data)

            if len(data) == amount:
                break

        if len(data) < amount:
            URL_BASE = scrape_next_page_link(response)

    create_news(data)
    return data
