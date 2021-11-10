from datetime import datetime
from rfeed import *
import requests
import json
import urllib.parse

branch = "articles"
repo = "lollo03.github.io"

r = requests.get("https://api.github.com/repos/lollo03/" +
                 repo + "/git/trees/" + branch + "?recursive=1")
resp = json.loads(r.text)

items = []

for i in resp["tree"]:
    if i["path"].startswith(".") or i["path"] == "portfolio.md":
        continue

    ogg = requests.get("https://raw.githubusercontent.com/lollo03/" +
                       repo + "/" + branch + "/" + i["path"])
    ogg = ogg.text
    ogg = ogg.split("<!--")[1]
    ogg = ogg.split("-->")[0]
    ogg = ogg.replace("\n", "")

    ogg = json.loads(ogg)

    link = "https://github.com/lollo03/lollo03.github.io/blob/articles/" + \
        urllib.parse.quote(i["path"])

    data = datetime.strptime(ogg["data"].replace(" ", ""), '%d/%m/%Y')

    items.insert(0, Item(
        title=ogg["titolo"],
        link=link,
        description=ogg["desc"],
        guid=Guid(ogg["titolo"]),
        pubDate=data
    ))


feed = Feed(
    title="RSS Feed Lorenzo Andreasi",
    link="https://lollo03.github.io",
    description="Feed del mio blog personale",
    language="it-IT",
    lastBuildDate=datetime.now(),
    items=items
)
f = open("rss.xml", "w")
f.write(feed.rss())
f.close()
