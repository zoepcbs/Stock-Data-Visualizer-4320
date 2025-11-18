import requests
import pygal
from lxml import etree
from datetime import datetime

class StockDataVisualizer:

    def __init__(self, api_key):

        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_symbol(self):

        symbol = input("Enter the stock symbol you are looking for:").upper().strip()
        return symbol
    
    def get_chart_type(self):

        print("\nChart Types:")
        print("\n--------------")
        print("1. Bar\n 2. Line")

        chart_type = input("Enter the chart type you want (1, 2):").strip()

        if chart_type == "1":
            return "bar"
        elif chart_type == "2":
            return "line"
        else:
            return "line"
        
    def get_time_series(self):
        print("Select the Time Series of the chart you want to generate:")
        print("\n----------------------------")
        print("\n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n")
        
        time_series = input("Enter time series option (1-4): ").strip()

        if time_series == "1":
            return "TIME_SERIES_INTRADAY"
        elif time_series == "2":
            return "TIME_SERIES_DAILY"
        elif time_series == "3":
            return "TIME_SERIES_WEEKLY"
        elif time_series == "4":
            return "TIME_SERIES_MONTHLY"
        else:
            return "TIME_SERIES_DAILY"
        
    def get_date_range(self):
        while True:
            start_date = input("Enter beginning date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                
                if end < start:
                    print("Error: End date cannot be before start date. Please try again.\n")
                    continue
                    
                return start_date, end_date
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD format.\n")
    
    def get_stock_data(self, symbol, function):
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "full"
        }
        
        if function == "TIME_SERIES_INTRADAY":
            params["interval"] = "60min"
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def filter_data_by_date(self, data, start_date, end_date, function):
        
        if function == "TIME_SERIES_INTRADAY":
            key = "Time Series (60min)"
        elif function == "TIME_SERIES_DAILY":
            key = "Time Series (Daily)"
        elif function == "TIME_SERIES_WEEKLY":
            key = "Weekly Time Series"
        elif function == "TIME_SERIES_MONTHLY":
            key = "Monthly Time Series"
        else:
            key = None
        
        if not key or key not in data:
            print("Error: Unable to find time series data")
            return None
        
        time_series = data[key]
        
        return {date_str: values 
                for date_str, values in time_series.items() 
                if start_date <= date_str.split()[0] <= end_date}