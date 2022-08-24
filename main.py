import requests
from twilio.rest import Client

STOCK_NAME = "IBM"
COMPANY_NAME = "IBM"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

newspoint_api_key = "your own newspoint api key"
alphavantage_api_key = "you rown alpha vantage api key"

def find_difference(stock1:float,stock2:float):
    if stock1 >= stock2:
        return stock1-stock2
    else:
        return stock2 - stock1


def stock_val_percentage(previous_stock_val):
    five_percent_stock_val = 5/100 * previous_stock_val
    return five_percent_stock_val


#ibm stock parameters
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": alphavantage_api_key
    
}

#api request call
alphavantage_response = requests.get(STOCK_ENDPOINT,params=stock_parameters)
alphavantage_response.raise_for_status()

data = alphavantage_response.json()
# print(data["Time Series (Daily)"])

#current and previous stock values
current_closing_stock_value = float(data["Time Series (Daily)"]['2022-08-18']["4. close"])
previous_closing_stock_value= float(data["Time Series (Daily)"]['2022-07-29']["4. close"])


#find stock difference
stock_difference = find_difference(current_closing_stock_value,previous_closing_stock_value)
up_down = None
if stock_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
    
#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent_diff = stock_difference/current_closing_stock_value *100

# if the value increase is greater than 5% recieve news
if percent_diff > 5:
    news_params ={
        "apiKey":newspoint_api_key,
        "q": COMPANY_NAME
        
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()['articles']
    first_three_articles = articles[:3]
    print(first_three_articles)



   #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{percent_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    #Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

#use your own virtual twilio number and verified phone number to recieve sms notification 
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
