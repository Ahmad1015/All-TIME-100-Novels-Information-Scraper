# All-TIME 100 Novels Information Scraper
This project retrieves the names of the "All-TIME 100 Novels" and uses the Wikipedia API to gather relevant information about each novel. The collected data is then stored in a pandas DataFrame and exported to an Excel file.

## Features
- Scrapes novel names from the TIME magazine's "All-TIME 100 Novels" list.
- Fetches relevant information (Author, Genre, Publisher, Publication date) for each novel from Wikipedia.
- Handles missing information by attempting to fetch data from Open Library.
- Stores data in a pandas DataFrame and exports it to an Excel file.
## Requirements
- Python 3.x
- requests library
- beautifulsoup4 library
- pandas library
## Installation
Install the required libraries using pip:
```bash
pip install requests beautifulsoup4 pandas
```
## How to Run
1. Clone the Repository and navigate to Directory:
```bash
https://github.com/Ahmad1015/All-TIME-100-Novels-Information-Scraper.git
cd All-TIME-100-Novels-Information-Scraper
```
2. Run the Script:
```python
python main.py
```
## Script Explanation
1. Scraping Novel Names:
- The script fetches the webpage containing the "All-TIME 100 Novels" list and extracts the names of the novels.
2. Fetching Wikipedia Links:
- For each novel, the script uses the Wikipedia API to get the Wikipedia page link.
3. Extracting Relevant Information:
- The script parses each Wikipedia page to extract the Author, Genre, Publisher, and Publication date.
- If any information is not available on Wikipedia, the script attempts to fetch it from Open Library.
4. Storing Data:
- The collected data is stored in a pandas DataFrame and exported to an Excel file named book_details.xlsx.
## Output
The script creates an Excel file named book_details.xlsx containing the relevant information for each novel.
## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Any contributions to improve the accuracy or functionality of the script are welcome.
