from bs4 import BeautifulSoup
import requests

# Getting the names of the books
web_page = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text

soup = BeautifulSoup(web_page, "html.parser")

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

# Getting relevant information of specific books from wikipedia
relevant_data = []
for index in range(len(wikipedia_link)):
    temp = wikipedia_link[index]
    wiki_data = requests.get(str(temp)).text
    soup = BeautifulSoup(wiki_data, "html.parser")
    t_body_element = soup.find(name="tbody")
    panel = t_body_element.find_all(name="td", class_="infobox-data")

    dict = {
        'author': t_body_element.find(class_="infobox-data").getText(),
        'language': panel[2].getText(),
        'genre': panel[3].getText(),
        'publisher': panel[4].getText(),
        'publication_date': panel[5].getText()[:-3],
        'print_available': panel[6].getText(),
        'pages': panel[7].getText(),
    }

    relevant_data.append(dict)
print(relevant_data)
