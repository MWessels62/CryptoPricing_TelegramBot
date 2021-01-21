from env import cmc_token
import requests

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {'X-CMC_PRO_API_KEY': cmc_token}
params = {'symbol': 'BTC', 'convert': 'USD'}

r = requests.get(url, headers=headers, params=params)
print(r.json())

def main():
    print(cmc_token)

if __name__ == "__main__":
    main()