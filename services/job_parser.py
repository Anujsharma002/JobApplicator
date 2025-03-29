import requests
from bs4 import BeautifulSoup


def parsed_data(url):
    url = url 
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True) 
        return text
    else:
        return "Failed to retrieve content"


