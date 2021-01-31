from env import cmc_token #Imports cmc_tokenvariable from the env.py file
from env import telegramToken
import requests
import json
from extract import json_extract

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {'X-CMC_PRO_API_KEY': cmc_token}  #Key is in the cmc_token variable
params = {'symbol': 'BTC', 'convert': 'USD'}

r = requests.get(url, headers=headers, params=params)
print(r.json())


def write_json(data, filename):
    filename_output = str(filename) + ".txt"
    with open(filename_output,'w') as json_output: 
        json.dump(data.json(),json_output)

def main():
    print(cmc_token)

def get_cmc_data(crypto_symbol):
    jsonFile = open("BitcoinPrice.txt",'r')
    values = json.load(jsonFile)
    jsonFile.close()
    print(values["data"]["BTC"]["quote"]["USD"]["price"])

def telegram_GetUpdates():
    updates = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getUpdates'))
    
    content = updates.json() #convert response to JSON format
    print(content)
    #content = json.load(updates.json())

    # ! Need to refine this to rather search by properly going through the nested sections -->  (updateText = content["result"]["message"]["text"])
    names = json_extract(updates.json(), 'text')
    print("The message is: ")
    print(names)


if __name__ == "__main__":
    main()
    write_json(r,"BitcoinPrice")
    get_cmc_data("BTC")
    telegram_GetUpdates()
    test = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegramToken, 'getMe'))
    print(test.json())

#Basic telegram query structure
#file = requests.get('https://api.telegram.org/bot{0}/{1}'.format(telegram_token, 'getMe'))
