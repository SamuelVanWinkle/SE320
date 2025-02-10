"""
Author: Samuel Van Winkle
File: stocks_vanwinkle.py
Help from ChatGPT
"""

import json
import sys
from requests import get
from datetime import date

def download_data(ticker: str) -> dict:
    """Gets data from the URL and returns a dictionary
    Args:
        ticker (str): Which stock's data is being retrieved
    """
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = get(base_url + path, headers=headers)
        data = response.json()

        if "data" in data and "tradesTable" in data["data"] and "rows" in data["data"]["tradesTable"]:
            closing_prices = [float(row["close"].replace('$', "")) for row in data["data"]["tradesTable"]["rows"]]
            max_price = max(closing_prices)
            min_price = min(closing_prices)
            avg_price = sum(closing_prices) / len(closing_prices)
            middle_index = len(closing_prices) // 2
            if len(closing_prices) % 2 == 0:
                med_price = (sorted(closing_prices)[middle_index - 1], sorted(closing_prices)[middle_index])
            else:
                med_price = (sorted(closing_prices)[middle_index])
            return {
                "min": min_price,
                "max": max_price,
                "avg": avg_price,
                "medium": med_price,
                "ticker": ticker
            }
        else:
            return []
    except Exception as e:
        print(e)    
        return {}

def create_json(filename: str, data: dict) -> None: 
    """Creates a Json file for the stock data"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=1)

tickers = sys.argv[1:]
complete_dict = []

for ticker in tickers:
    ticker = ticker.upper()
    data_dict = download_data(ticker)
    complete_dict.append(data_dict)
    #complete_dict[ticker] = data_dict

create_json("stocks.json", complete_dict) 