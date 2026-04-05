import requests
from bs4 import BeautifulSoup
import os

URL = "https://sp.pokepara.jp/tokyo/m9/a10034/shop4995/gal/777801/blog/"
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

def send_discord(title, link, img):
    data = {
        "embeds": [
            {
                "title": "新着ブログ！",
                "description": title,
                "url": link,
                "image": {"url": img} if img else {},
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=data)

def get_latest():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    article = soup.select_one(".blog_list li")
    if not article:
        return None, None, None

    title = article.get_text(strip=True)

    link_tag = article.find("a")
    link = link_tag["href"] if link_tag else ""
    if link.startswith("/"):
        link = "https://sp.pokepara.jp" + link

    img_tag = article.find("img")
    img = img_tag["src"] if img_tag else None
    if img and img.startswith("/"):
        img = "https://sp.pokepara.jp" + img

    return title, link, img

def main():
    title, link, img = get_latest()
    if not title:
        return

    latest = title + link

    try:
        with open("last.txt", "r") as f:
            old = f.read()
    except:
        old = ""

    if latest != old:
        send_discord(title, link, img)
        with open("last.txt", "w") as f:
            f.write(latest)

if __name__ == "__main__":
    main()
