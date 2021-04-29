import json
import time
import urllib  # ( urllib.parse.quote_plus(text)) allows us to handle special characters in the API URL

import dateutil.parser
import requests

from env import cmc_token  # Imports cmc_tokenvariable from the env.py file
from env import telegramToken
from extract import json_extract

#FEATURES
#Bi-directional API calls, with and without additional parameters
#TIme package "listening"
#echo reply exception

def fetchCryptoPrice(symbol,chat):
    symbol = symbol.upper()
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': cmc_token}  #Key is in the cmc_token variable
    params = {'symbol': symbol, 'convert': 'USD'}

    r = requests.get(url, headers=headers, params=params)
    response_json = r.json()
    
    last_updated = dateutil.parser.parse(response_json["data"][symbol]["quote"]["USD"]["last_updated"])
    price = round(r.json()["data"][symbol]["quote"]["USD"]["price"],2) #Extract price from JSON response and round to 2 decimal points
    chatbotResponse = f"The price for {symbol}, as of {last_updated} is ${price}"
    return(telegramReturnPrice(chatbotResponse,chat))

#FUNCTIONALITY TO WRITE DATA TO A FILE, NOT CURRENTLY BEING USED
#def writeJson(data, filename):
#    filename_output = str(filename) + ".txt"
#    open(filename_output, 'w').close() # ? This clears the content of the text file, this needs to be removed once I am able to handle multiple messages
#    with open(filename_output,'w') as json_output: 
#        json.dump(data,json_output)

def telegramGetUpdates(offset=None):
    URL = 'https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getUpdates')
    URL += "?timeout=100" #Adding this introduces long-polling to reduce resource demands
    if offset:
        URL += "&offset={}".format(offset)
    updates = requests.get(URL) #added an offsets parameter, which contains the value of the latest update_id so that messages already processed will not be sent again
    return updates.json()
 

 
def telegramReturnPrice(text,chat):
    text = urllib.parse.quote_plus(text) #allows us to handle special characters in the API URL
    parameterInput = "?chat_id={}&text={}".format(chat,text)
    sendMessage = requests.get('https://api.telegram.org/bot{}/{}{}'.format(telegramToken, 'sendMessage',parameterInput)) # 


def getLastUpdateId(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echoAll(updates):
    #try:
    for update in updates["result"]:
        text1 = update["message"]["text"]
        chat = update["message"]["chat"]["id"] 
        try:
            fetchCryptoPrice(text1,chat)
        except Exception as e:
            if text1 == "/start":
                telegramReturnPrice("Welcome to the Crypto Price Bot. Type in a crypto symbol, e.g. BTC, or ETH to get the current price.", chat)
                telegramReturnPrice("Here are some of the top crypto symbols that you can use: BTC - Bitcoin |||| ETH - Etherium |||| USDT - Tether |||| DOT - Polkadot |||| ADA - Cardano", chat)
            elif text1.startswith("/"):
                return
            else:
                errorText = "There was an error in retrieving the crytocurrency price. Please make sure that you are using the correct symbol and try again"
                telegramReturnPrice(errorText,chat)
                print(e)

def main():
    print("Telegram crypto price bot currently running!!!!!!!!!!!")
    lastUpdateId = None
    while True: 
        updates = telegramGetUpdates(lastUpdateId)
        if len(updates["result"]) > 0:
            lastUpdateId = getLastUpdateId(updates) + 1
            echoAll(updates)


        time.sleep(0.5)   #only repeats every 1 second


if __name__ == '__main__':
    main()

