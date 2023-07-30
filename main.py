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
    wiki_data = requests.get(temp).text
    soup = BeautifulSoup(wiki_data, "html.parser")
    try:
        t_body_element = soup.find(name="tbody")
        panel = t_body_element.find_all(name="td", class_="infobox-data")

        # Function to extract relevant data
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


        # Function to fetch data from Open Library if not available in Wikipedia
        def not_available(link, find):
            # fetching name of the book from wikipedia's First heading
            name = requests.get(url=link).text
            wiki_soup = BeautifulSoup(name,"html.parser")
            name = wiki_soup.find(name="i").getText()

            # fetching data from Open Library
            base_url = 'http://openlibrary.org/search.json'
            params = {'q': name}
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                docs = data.get('docs', [])

                for book in docs:
                    if find == "Author":
                        return (book.get('author_name', ['N/A']))[0]
                    elif find == "Genre":
                        return (book.get('subject', ['N/A']))[0]
                    elif find == "Publisher":
                        return (book.get('publisher', 'N/A'))[0]
                    elif find == "Publishing_date":
                        return (book.get('publish_date', 'N/A'))[0]
                    elif find == "Pages":
                        return (book.get('number_of_pages', 'N/A'))[0]
                    else:
                        return "Data not Available"

            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        # Getting Author name
        author = relevant_data(t_body_element, "Author")
        if author == "Data not Available":
            author = not_available(temp,"Author")

        # Getting Genre of the book
        genre = relevant_data(t_body_element, 'Genre')
        if genre == "Data not Available":
            genre = not_available(temp,"Genre")

        # Getting the publisher name
        publisher = relevant_data(t_body_element, 'Publisher')
        if publisher == "Data not Available":
            publisher = not_available(temp,"Publisher")

        # Getting the publishing date of the book
        publishing_date = relevant_data(t_body_element, "Publication date")
        if publishing_date[-3:] == "[1]":
            publishing_date = publishing_date.replace("[1]", "")
        if publishing_date == "Data not Available":
            publishing_date = not_available(temp,"Publishing_date")

        # Getting the number of pages of the book
        pages = relevant_data(t_body_element, "Pages")
        if pages == "Data not Available":
            pages = not_available(temp,"Pages")
    except:
        # Set data to "Data not Available" if an error occurs during parsing
        genre = pages = publishing_date = author = publisher = "Data not Available"

    dict = {
        'Author': author,
        'Genre': genre,
        'Publisher': publisher,
        'Publication_date': publishing_date,
    }

    relevant_data_list.append(dict)

# Create a DataFrame from the list of book information
df = pandas.DataFrame(relevant_data_list)

# Export the DataFrame to Excel
df.to_excel('book_details.xlsx', index=False)

