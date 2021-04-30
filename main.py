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

def fetchCryptoPrice(symbol,chat): #Fetches the price from the CoinMarketCap API based on crypto symbol provided by the user.
    symbol = symbol.upper() #Make uppercase to cater for differences in case
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': cmc_token}  #Key is in the cmc_token variable
    params = {'symbol': symbol, 'convert': 'USD'}

    #API request
    r = requests.get(url, headers=headers, params=params)
    response_json = r.json()
    
    
    last_updated = dateutil.parser.parse(response_json["data"][symbol]["quote"]["USD"]["last_updated"]) #Gets the update time for latest API response
    price = round(r.json()["data"][symbol]["quote"]["USD"]["price"],2) #Extract price from JSON response and round to 2 decimal points
    chatbotResponse = f"The price for {symbol}, as of {last_updated} is ${price}" #create message to be sent back to Telegram bot
    return(telegramResponseMessage(chatbotResponse,chat))

#FUNCTIONALITY TO WRITE DATA TO A FILE, NOT CURRENTLY BEING USED
#def writeJson(data, filename):
#    filename_output = str(filename) + ".txt"
#    open(filename_output, 'w').close() # ? This clears the content of the text file, this needs to be removed once I am able to handle multiple messages
#    with open(filename_output,'w') as json_output: 
#        json.dump(data,json_output)

def telegramGetUpdates(offset=None): #This is run repeatedly to communicate with Telegram API to see if there is new user input
    URL = 'https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getUpdates')
    URL += "?timeout=100" #Adding this introduces long-polling to reduce resource demands
    if offset:
        URL += "&offset={}".format(offset) #added an offsets parameter, which contains the value of the latest update_id so that messages already processed will not be sent again
    updates = requests.get(URL) 
    return updates.json()
 

def telegramResponseMessage(responseText,chat): #Used to send a response message (provided in 'text' variable) back to the Telegram bot
    responseText = urllib.parse.quote_plus(responseText) #allows us to handle special characters in the API URL
    parameterInput = "?chat_id={}&text={}".format(chat,responseText)
    sendMessage = requests.get('https://api.telegram.org/bot{}/{}{}'.format(telegramToken, 'sendMessage',parameterInput)) # 


def getLatestTelegramUpdateId(updates): #gets the update_id for the latest update received in the JSON message, since the JSON message can include multiple recent requests even if some of them have been recived before
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echoAll(updates): #is initiated whenever it detects a new update from Telegram API, then determines how to respond
    #try:
    for update in updates["result"]:
        text1 = update["message"]["text"]
        chat = update["message"]["chat"]["id"] 
        firstName = update["message"]["chat"]["first_name"]
        try:
            fetchCryptoPrice(text1,chat)
        except Exception as e:
            if text1 == "/start":  #'start' is used to initiate a bot conversation in Telegram
                telegramResponseMessage("Welcome, to the Crypto Price Bot {}!.".format(firstName), chat)
                telegramResponseMessage("Type in a crypto symbol, e.g. BTC, or ETH to get the current price.", chat)
                telegramResponseMessage("Here are some of the top crypto symbols that you can use: BTC - Bitcoin |||| ETH - Etherium |||| USDT - Tether |||| DOT - Polkadot |||| ADA - Cardano", chat)
            elif text1.startswith("/"):
                return
            else:
                errorText = "There was an error in retrieving the crytocurrency price. Please make sure that you are using the correct symbol and try again"
                telegramResponseMessage(errorText,chat)

def main():
    print("Telegram crypto price bot currently running!!!!!!!!!!!")
    latestTelegramUpdateId = None
    while True: 
        updates = telegramGetUpdates(latestTelegramUpdateId)
        if len(updates["result"]) > 0:
            latestTelegramUpdateId = getLatestTelegramUpdateId(updates) + 1
            echoAll(updates)
        time.sleep(0.5)   #only repeats every 1 second, to reduce resource load


if __name__ == '__main__':
    main()

