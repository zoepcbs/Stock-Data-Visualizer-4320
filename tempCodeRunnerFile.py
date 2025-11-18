import requests
import pygal
from lxml import etree
from datetime import datetime

class StockDataVisualizer:

    def __init__(self, api_key):

        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_symbol(self):

        symbol = input("Enter the stock symbol you are looking for: ").upper().strip()
        return symbol
    
    def get_chart_type(self):

        print("\nChart Types:")
        print("\n--------------")
        print("1. Bar\n2. Line")

        chart_type = input("Enter the chart type you want (1, 2): ").strip()

        if chart_type == "1":
            return "bar"
        elif chart_type == "2":
            return "line"
        else:
            return "line"
        
    def get_time_series(self):
        print("Select the Time Series of the chart you want to generate: ")
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
            print(f"Error obtaining data: {e}")
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
    
    def make_chart(self, symbol, filtered_data, chart_type, start_date, end_date):

        if not filtered_data:
            print("No data to display for the selected date range")
            return
        
        sorted_dates = sorted(filtered_data.keys())
        dates = [d.split()[0] for d in sorted_dates]
        opens = [float(filtered_data[d]["1. open"]) for d in sorted_dates]
        highs = [float(filtered_data[d]["2. high"]) for d in sorted_dates]
        lows = [float(filtered_data[d]["3. low"]) for d in sorted_dates]
        closes = [float(filtered_data[d]["4. close"]) for d in sorted_dates]
        
        chart = pygal.Bar() if chart_type == "bar" else pygal.Line()
        chart.title = f'Stock Data for {symbol}: {start_date} to {end_date}'
        chart.x_labels = dates
        
        chart.add('Open', opens)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Close', closes)
        
        filename = f"stock_chart_{symbol}.svg"
        chart.render_to_file(filename)
        
        try:
            tree = etree.parse(filename)
            print(f"\nChart generated successfully: {filename}")
            print(f"SVG validated with lxml - Root element: {tree.getroot().tag}")
        except etree.XMLSyntaxError as e:
            print(f"Warning: SVG validation failed: {e}")
            print(f"Chart generated: {filename}")
        
        print("Opening chart in browser...")
        chart.render_in_browser()

    def run(self):
        print("=========================================")
        print("\nStock Data Visualization Application\n")
        print("=========================================")
        
        symbol = self.get_stock_symbol()
        chart_type = self.get_chart_type()
        time_series = self.get_time_series()
        start_date, end_date = self.get_date_range()
        
        print(f"\nGetting data for {symbol}...")
        data = self.get_stock_data(symbol, time_series)
        
        if data and "Error Message" not in data and "Note" not in data:
            filtered_data = self.filter_data_by_date(data, start_date, end_date, time_series)
            if filtered_data:
                self.generate_chart(symbol, filtered_data, chart_type, start_date, end_date)
            else:
                print("No data found for the specified date range.")
        else:
            print("Error: Unable to obtain stock data. Please check the symbol and try again.")
            if data and "Note" in data:
                print("Note: API call frequency limit may have been reached.")

def main():
    API_KEY = "8VZH0REUTT28GS5M"
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Please obtain an API key from Alpha Vantage and update the API_KEY variable")
        return
    
    visualizer = StockDataVisualizer(API_KEY)
    visualizer.run()


if __name__ == "__main__":
    main()