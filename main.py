from bs4 import BeautifulSoup
import requests

web_page = requests.get("https://entertainment.time.com/2005/10/16/all-time-100-novels/slide/all/").text

soup = BeautifulSoup(web_page,"html.parser")

div_tag = soup.find(class_="entry-content group")





names = [item.getText() for item in div_tag.find_all("i")]
print(names)