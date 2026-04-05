import requests
from bs4 import BeautifulSoup
import os

# ブログURL
URL = "https://sp.pokepara.jp/tokyo/m9/a10034/shop4995/gal/777801/blog/"

# 前回記事タイトルを取得
last_file = "last.txt"
try:
    with open(last_file, "r") as f:
        last_title = f.read().strip()
except:
    last_title = ""

# 最新記事取得
res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")
article = soup.select_one(".blog_list li")

if article:
    title = article.get_text(strip=True)
    link_tag = article.find("a")
    link = link_tag["href"] if link_tag else ""
    if link.startswith("/"):
        link = "https://sp.pokepara.jp" + link
    img_tag = article.find("img")
    img = img_tag["src"] if img_tag else ""
    if img.startswith("/"):
        img = "https://sp.pokepara.jp" + img

    # 新着かチェック
    if title != last_title:
        # 新着あり
        print(f"::set-output name=new::true")
        print(f"::set-output name=title::{title}")
        print(f"::set-output name=link::{link}")
        print(f"::set-output name=img::{img}")

        # 次回用に last.txt を更新
        with open(last_file, "w") as f:
            f.write(title)
    else:
        print("::set-output name=new::false")
else:
    print("::set-output name=new::false")
