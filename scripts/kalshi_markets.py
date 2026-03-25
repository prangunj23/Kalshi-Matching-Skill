import requests
import time
import json

TICKERS = ["NCAAMB", "NBA", "NCAAWB", "EUROLEAGUE", "CBA", "ABA", "GBL", "NBL", "ARGLNB", 
           "MLB", "NCAABB", "WTA", "ATP", "UCLW", "UCL", "NHL"]
    
def get_markets(series_ticker):
    valid_markets = []
    url = "https://api.elections.kalshi.com/trade-api/v2/markets"

    params = {
        "limit": 1000,
        "status": "open",
        "mve_filter": "exclude",
        "series_ticker": series_ticker
    }
    response = requests.get(url, params=params)
    data = response.json()
    cursor = data.get('cursor')

    while True:
        if 'markets' not in data:
            print(data)
            break
        for market in data['markets']:
            valid_markets.append({
                "ticker": market['ticker'],
                "rules_primary": market["rules_primary"],
                "rules_secondary": market["rules_secondary"]
            })
        if cursor == '':
            break
        
        params['cursor'] = cursor
        response = requests.get(url, params=params)
        data = response.json()
        cursor = data.get('cursor')
    
    return valid_markets

def get_series():
    url = "https://api.elections.kalshi.com/trade-api/v2/series?category=Sports"

    response = requests.get(url)
    data = response.json()
    series_tickers = []

    for series in data["series"]:
        if any(ticker in series['ticker'] for ticker in TICKERS):
            series_tickers.append(series["ticker"])
    return series_tickers


def main():
    market_tickers = []
    series_tickers = get_series()
    for ticker in series_tickers:
        market_tickers = market_tickers + get_markets(ticker)
        time.sleep(0.25)
    print(json.dumps(market_tickers, indent=2))



if __name__ == "__main__":
    main()
