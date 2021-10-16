import datetime
from rfeed import *
import requests
import json

branch = "articles"
repo = "lollo03.github.io"

r = requests.get("https://api.github.com/repos/lollo03/" +
                 repo + "/git/trees/" + branch + "?recursive=1")
resp = json.loads(r.text)

items = []

for i in resp["tree"]:
    if i["path"] == ".gitignore" or i["path"] == "portfolio.md":
        continue
    titolo = i["path"].split(".")[0].split("-")[1].lstrip(" ")

    desc = requests.get("https://raw.githubusercontent.com/lollo03/" +
                        repo + "/" + branch + "/" + i["path"])
    desc = desc.text
    desc = desc.split("<!--")[1]
    desc = desc.split("-->")[0]
    desc = desc.replace("\n", "")

    items.insert(0, Item(
        title=titolo,
        link="https://lollo03.github.io",
        description=desc
    ))


feed = Feed(
    title="RSS Feed Lorenzo Andreasi",
    link="https://lollo03.github.io",
    description="Feed del mio blog personale",
    language="it-IT",
    lastBuildDate=datetime.datetime.now(),
    items=items
)
f = open("rss.xml", "w")
f.write(feed.rss())
f.close()
