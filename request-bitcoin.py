import requests

def get_crypto_prices(coin_ids, vs_currency="usd"):
    # coin_ids مثل "bitcoin,ethereum,stellar"
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_ids,
        "vs_currencies": vs_currency
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("خطا در درخواست:", response.status_code)
        return None

def main():
    coins = "bitcoin,ethereum,stellar"
    data = get_crypto_prices(coins, "usd")
    if data:
        # داده‌ای که برمی‌گرده شبیه این شکل خواهد بود:
        # {
        #     "bitcoin": {"usd": 50000},
        #     "ethereum": {"usd": 3000},
        #     "stellar": {"usd": 0.12}
        # }
        for coin, info in data.items():
            price = info.get("usd")
            print(f"قیمت {coin} در دلار: {price}")

if __name__ == "__main__":
    main()
