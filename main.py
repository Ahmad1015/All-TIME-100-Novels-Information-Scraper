from bs4 import BeautifulSoup
import requests
import pandas

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

    link = response[-1][0]
    if "_(film)" in link:
        link = link.replace("_(film)", "")
    if "(comics)" in link:
        link = link.replace("(comics)", "")
    wikipedia_link.append(link)

# Getting relevant information of specific books from wikipedia
relevant_data_list = []
for index in range(len(wikipedia_link)):
    temp = wikipedia_link[index]
    temp = temp
    wiki_data = requests.get(temp).text
    soup = BeautifulSoup(wiki_data, "html.parser")
    try:
        t_body_element = soup.find(name="tbody")
        panel = t_body_element.find_all(name="td", class_="infobox-data")


        def relevant_data(t_body, name):
            try:
                label = t_body.find('th', string=name)
                if label:
                    # If the label is found, navigate to the adjacent 'td' tag to extract the genre text
                    data = label.find_next('td').get_text(strip=True)
                    return data
            except:
                pass
            return "Data not Available"


        # Getting Author name
        author = relevant_data(t_body_element, "Author")

        # Getting Genre of the book
        genre = relevant_data(t_body_element, 'Genre')

        # Getting the publisher name
        publisher = relevant_data(t_body_element, 'Publisher')

        # Getting the publishing date of the book
        publishing_date = relevant_data(t_body_element, "Publication date")
        if publishing_date[-3:] == "[1]":
            publishing_date = publishing_date.replace("[1]", "")

        # Getting the number of pages of the book
        pages = relevant_data(t_body_element, "Pages")
    except:
        genre = pages = publishing_date = author = publisher = "Data not Available"

    dict = {
        'Author': author,
        'Genre': genre,
        'Publisher': publisher,
        'Publication_date': publishing_date,
    }

    relevant_data_list.append(dict)

df = pandas.DataFrame(relevant_data_list)
df.to_excel('book_details.xlsx', index=False)
