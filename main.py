import requests
from bs4 import BeautifulSoup
import os

URL = "https://sp.pokepara.jp/tokyo/m9/a10034/shop4995/gal/777801/blog/"
LAST_FILE = "last.txt"

# 前回記事を取得
try:
    with open(LAST_FILE, "r") as f:
        last_title = f.read().strip()
except:
    last_title = ""

res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")
article = soup.select_one(".blog_list li")

# 出力用関数（GitHub Actions 環境ファイル方式）
def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"{name}={value}\n")

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

    if title != last_title:
        # 新着あり
        set_output("new", "true")
        set_output("title", title)
        set_output("link", link)
        set_output("img", img)

        # last.txt を更新
        with open(LAST_FILE, "w") as f:
            f.write(title)
    else:
        set_output("new", "false")
else:
    set_output("new", "false")
