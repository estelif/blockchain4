import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CryptoPanicAPI:
    BASE_URL = "https://cryptopanic.com/api/v1/"
    
    def __init__(self):
        self.api_key = os.getenv("CRYPTO_PANIC_API_KEY")
        if not self.api_key:
            raise ValueError("CryptoPanic API key not found in environment variables")
    
    def get_news(self, coin=None, filter="hot"):
        params = {
            "auth_token": self.api_key,
            "public": "true",
            "filter": filter
        }
        if coin:
            params["currencies"] = coin.upper()
        
        response = requests.get(f"{self.BASE_URL}posts/", params=params)
        response.raise_for_status()
        return response.json().get("results", [])

class CoinMarketCapAPI:
    BASE_URL = "https://pro-api.coinmarketcap.com/v1/"
    
    def __init__(self):
        self.api_key = os.getenv("COINMARKETCAP_API_KEY")
        if not self.api_key:
            raise ValueError("CoinMarketCap API key not found in environment variables")
        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key
        }
    
    def get_top_coins(self, limit=50):
        params = {
            "start": 1,
            "limit": limit,
            "convert": "USD"
        }
        response = requests.get(
            f"{self.BASE_URL}cryptocurrency/listings/latest",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_coin_data(self, symbol):
        params = {
            "symbol": symbol.upper(),
            "convert": "USD"
        }
        response = requests.get(
            f"{self.BASE_URL}cryptocurrency/quotes/latest",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        data = response.json().get("data", {})
        return data.get(symbol.upper()) if data else None