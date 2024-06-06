import requests
from bs4 import BeautifulSoup

def get_stock_price():
    url = "https://finance.yahoo.com/quote/TSLA/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_span = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        if price_span:
            return price_span.text
    return None
