from bs4 import BeautifulSoup
import requests



web_page = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text

soup = BeautifulSoup(web_page,"html.parser")

div_tag = soup.find(class_="entry-content group")

names = [item.getText() for item in div_tag.find_all("i")]

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

    print(response[-1])










'''wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

link_list = []




for x in range(0,len(names)):
    page_py = wiki_wiki.page(names[x])
    print("Page - Exists: %s" % page_py.exists())
    if not page_py.exists():
        print(names[x])
print(page_py.fullurl)

page_py = wiki_wiki.page('Python_(programming_language)')
print("Page - Exists: %s" % page_py.exists())
link_list.append(page_py.fullurl)'''






