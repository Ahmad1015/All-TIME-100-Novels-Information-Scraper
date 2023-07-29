from bs4 import BeautifulSoup
import requests


# Getting the names of the books
web_page = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text

soup = BeautifulSoup(web_page,"html.parser")

div_tag = soup.find(class_="entry-content group")

names = [item.getText() for item in div_tag.find_all("i")]

# Getting the wikipedia link of the books
wikipedia_link = []

for item in names:
    S = requests.Session()

    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": item,
        "limit": "1",
        "format": "json"
    }

    response = S.get(url="https://en.wikipedia.org/w/api.php", params=PARAMS).json()

    wikipedia_link.append(response[-1])




















