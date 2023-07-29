from bs4 import BeautifulSoup
import requests

web_page = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text

soup = BeautifulSoup(web_page,"html.parser")

names = [item.getText() for item in soup.find_all(name = "i")]
for item in range(len(names)):
    print(f'book {names[item]} and the count is {item}')