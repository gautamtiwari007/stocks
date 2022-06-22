import requests
import pprint
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "90GK147J4SFXP4SD"
NEW_API_KEY = "b256b9fc3bb044f5b38f785df84051e3"
TWILIO_SID = "AC4327cfa6f6cb0ce4707e396e63f1aa49"
TWILIO_AUTH_TOKEN = "72a5c95d729381a399636ec78cdb38ab"

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "⬆📈️"
else:
    up_down = "⬇️📉"


diff_percent = round((abs(difference) / yesterday_closing_price) * 100)

if diff_percent > 5:
    news_params = {
        'apiKey': NEW_API_KEY,
        'qInTitle': COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \n{article['description']}" for article in three_articles]
    pprint.pprint(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+13514449832",
            to="+917317464093"
        )
