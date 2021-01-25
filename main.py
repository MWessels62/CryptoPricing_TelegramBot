from env import cmc_token #Imports cmc_tokenvariable from the env.py file
import requests
import json

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

if __name__ == "__main__":
    main()
    write_json(r,"BitcoinPrice")
    get_cmc_data("BTC")