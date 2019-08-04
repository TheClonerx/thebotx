import urllib.request
import urllib.parse
import json
import html
import bs4
import config
clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

if not args:
    pharagraph = ""
    while not pharagraph.strip():
        response = urllib.request.urlopen(
            "http://{}.wikipedia.org/".format(clang)
        )
        soup = bs4.BeautifulSoup(response.read(), "html.parser")
        url = soup.find(id="n-randompage")
        response = urllib.request.urlopen(
            "http://{}.wikipedia.org{}".format(clang, url.a["href"])
        )
        soup = bs4.BeautifulSoup(response.read(), "html.parser")
        title = soup.find(id="firstHeading").get_text()
        content = soup.find(id="mw-content-text")
        pharagraph = content.div.p.get_text()
    if len(pharagraph) > 350:
        pharagraph = pharagraph[:350] + "..."
    msg = "<b>{}</b> (Random): {}".format(
        html.escape(title),
        html.escape(pharagraph)
    )
else:
    title = urllib.parse.quote(msgdata[1])
    url = (
        "https://{}.wikipedia.org/w/api.php?"
        "format=json&formatversion=2&action=query&prop=extracts&exintro="
        "&exchars=350&explaintext=&titles={}"
    ).format(clang, title)
    headers = {"Api-User-Agent": "TheBotx/5.0"}
    request = urllib.request.Request(url, None, headers, "GET")
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode())
    page = data["query"]["pages"][0]
    msg = "<b>{}</b>: {}".format(
        html.escape(page["title"]),
        html.escape(
            page["extract"]
        ) if "missing" not in page and page["extract"] != "..." else "<i>Missing page</i>"
    )
room.message(msg, html=True)
