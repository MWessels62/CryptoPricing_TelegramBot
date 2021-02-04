from env import cmc_token #Imports cmc_tokenvariable from the env.py file
from env import telegramToken
import requests
import json
from extract import json_extract

# telegram_GetUpdates - run to get latest quotes typed into Telegram
# use write_json to write this full json into a text file
# get_cmc_data - to fetch the symbole from the JSON 
# fetchCryptoPrice(symbol) - fetch just the symbol from the text file and run a request for price

#To-do: Error handling for incorrect symbol
#Handle multiple incoming messages



def fetchCryptoPrice(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {'X-CMC_PRO_API_KEY': cmc_token}  #Key is in the cmc_token variable
    params = {'symbol': symbol, 'convert': 'USD'}

    r = requests.get(url, headers=headers, params=params)
    response_json = r.json()
    print(response_json)
    last_updated = response_json["data"][symbol]["quote"]["USD"]["last_updated"] 
    price = round(r.json()["data"][symbol]["quote"]["USD"]["price"],2) #Extract price from JSON response and round to 2 decimal points
    chatbotResponse = f"The price for {symbol}, as of {last_updated} is ${price}"
    print(chatbotResponse) 
    return(telegram_returnprice(chatbotResponse))

#def read_file():
#   f = open("BitcoinQuote.txt", 'r')
#    file_contents = f.read()
#    print("The contents of the text file is: ")
#    print (file_contents)
#    f.close()


def write_json(data, filename):
    filename_output = str(filename) + ".txt"
    open(filename_output, 'w').close() # ? This clears the content of the text file, this needs to be removed once I am able to handle multiple messages
    with open(filename_output,'w') as json_output: 
        json.dump(data,json_output)


def main():
    print(cmc_token)


def get_cmc_data(): # ! This only returns the first crypto symbol from the file
    jsonFile = open("BitcoinQuote.txt",'r') # ! change hard-coded values
    values = json.load(jsonFile)
    jsonFile.close()

    num_updates = len(values["result"])
    last_update = num_updates - 1
    global chatId
    chatId=values["result"][last_update]["message"]["chat"]["id"]
    
    quote = json_extract(values, 'text')
    #print(values["data"][quote[0]]["quote"]["USD"]["price"])
    return fetchCryptoPrice(quote[-1])

def telegram_GetUpdates():
    updates = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getUpdates'))
    print("Original telegram message")

    print(updates.json())
    #content = updates.json() #convert response to JSON format
    #print(content)
    #content = json.load(updates.json())

    # ! Need to refine this to rather search by properly going through the nested sections -->  (updateText = content["result"]["message"]["text"])
    # ! For now this assumes that only one ticker symbol will come through at a time

    return write_json(updates.json(),"BitcoinQuote") # ! This writes the whole JSON to file - check if this is what is required 
    
def telegram_returnprice(text):
    
    #chatId = '@MW_CryptoPriceBot'
    text = "'" + text + "'"
    parameterInput = "?chat_id={}&text={}".format(chatId,text)
    print("The API call is {}".format('https://api.telegram.org/bot{}/{}{}'.format(telegramToken, 'sendMessage',parameterInput)))
    sendMessage = requests.get('https://api.telegram.org/bot{}/{}{}'.format(telegramToken, 'sendMessage',parameterInput)) # OLD TEXT - data ={'chat_id':'@MW_CryptoPriceBot','text':'{text}'} 
    print(sendMessage)
    content = sendMessage.content.decode("utf8")
    print(content)
    #return content

if __name__ == "__main__":
    main()
    telegram_GetUpdates()
    get_cmc_data()
     
    
    
    #test = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getMe'))
    #print(test.json())

#Basic telegram query structure
#file = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegram_token, 'getMe'))
