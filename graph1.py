import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

# define function to get stock data from Alpha Vantage API
def get_stock_data(symbol, time_series, start_date, end_date, api_key):
    base_url = "https://www.alphavantage.co/query"
    payload = {
        "function": time_series,
        "symbol": symbol,
        "outputsize": "full",
        "apikey": api_key
    }
    if time_series == 'TIME_SERIES_INTRADAY':
        payload['interval'] = '5min'
    elif time_series == 'TIME_SERIES_WEEKLY':
        payload['datatype'] = 'json'
    elif time_series == 'TIME_SERIES_DAILY':
        payload['datatype'] = 'csv'

    response = requests.get(base_url, params=payload)
    response.raise_for_status()

    if time_series == 'TIME_SERIES_WEEKLY':
        data = json.loads(response.text)
        time_series = 'Weekly Time Series'
        open_key = '1. open'
        high_key = '2. high'
        low_key = '3. low'
        close_key = '4. close'
    elif time_series == 'TIME_SERIES_DAILY':
        data = response.text.split('\n')
        data = [x.split(',') for x in data]
        data.pop()
        data.pop(0)
        data = data[::-1]
        time_series = 'Time Series (Daily)'
        open_key = '1. open'
        high_key = '2. high'
        low_key = '3. low'
        close_key = '4. close'
    elif time_series == 'TIME_SERIES_MONTHLY':
        data = json.loads(response.text)
        time_series = 'Monthly Time Series'
        open_key = '1. open'
        high_key = '2. high'
        low_key = '3. low'
        close_key = '4. close'
    else:
        raise ValueError("Invalid time series")

    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for row in data:
        date_str = row[0]
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date >= start_date and date <= end_date:
            dates.append(date)
            open_str = row[1]
            high_str = row[2]
            low_str = row[3]
            close_str = row[4]
            open_prices.append(float(open_str))
            high_prices.append(float(high_str))
            low_prices.append(float(low_str))
            close_prices.append(float(close_str))

    return dates, open_prices, high_prices, low_prices, close_prices



# ask user for input and loop until valid input is given
while True:
    try:
        symbol = input("Enter stock symbol: ")
        time_series = input("Enter time series (Intraday, Daily, Weekly, Monthly): ")
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")
        graph_type = input("Enter type of graph (line, bar): ")
        api_key = '4UCAG7K56D1Z76GB'

        # convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # get stock data from Alpha Vantage API
        dates, open_prices, high_prices, low_prices, close_prices = get_stock_data(symbol, f'TIME_SERIES_{time_series.upper()}', start_date, end_date, api_key)

        # plot graph
        fig, ax = plt.subplots(figsize=(10, 5))

        if graph_type == 'line':
            ax.plot(dates, open_prices, label="Open")
            ax.plot(dates, high_prices, label="High")
            ax.plot(dates, low_prices, label="Low")
            ax.plot(dates, close_prices, label="Close")
        elif graph_type == 'bar':
            ax.bar(dates, open_prices, label="Open")
            ax.bar(dates, close_prices, label="Close")
        else:
            raise ValueError("Invalid graph type")

        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.set_title(f"{symbol} Stock Prices")

        ax.legend()
        plt.show()

        # ask user if they want to search for another stock price
        choice = input("Do you want to search for another stock price? (y/n) ")
        if choice.lower() != 'y':
            break

    except (requests.exceptions.HTTPError, ValueError, KeyError, json.JSONDecodeError, KeyboardInterrupt) as e:
        print(f"Error: {e}")
        print("Please try again\n")