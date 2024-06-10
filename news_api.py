import requests
from deep_translator import GoogleTranslator

def get_news():
    # Параметры запроса к NewsAPI
    news_url = 'https://newsapi.org/v2/everything'
    news_params = {
        'q': 'tesla',
        'from': '2024-05-15',
        'to': '2024-05-20',
        'sortBy': 'publishedAt',
        'apiKey': '3e80c401d12e43c38d803f68eca80e01'
    }

    response = requests.get(news_url, params=news_params)
    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        return None

def translate_news(articles):
    translator = GoogleTranslator(source='auto', target='ru') #автоопределение исходного языка 
    translated_articles = [] #для хранения переведенных статей

    for article in articles:
        title = article['title'] 
        translated_title = translator.translate(title)  
        article['title'] = translated_title
        translated_articles.append(article)
    return translated_articles


