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