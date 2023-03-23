import requests
import json
import pygal
import webbrowser
from datetime import datetime
from lxml import etree

# Prompt the user for the stock symbol they want data for
symbol = input("Enter the stock symbol for the company you want data for: ")

# Prompt the user for the chart type they would like
print("Enter the chart type you would like:")
print("1. Line")
print("2. Bar")
chart_choice = int(input("Choice: "))
if chart_choice == 1:
    chart_type = "line"
elif chart_choice == 2:
    chart_type = "bar"
else:
    print("Error: invalid chart type.")
    exit()

# Prompt the user for the time series function they want to use
print("Enter the time series function you want to use:")
print("1. DAILY")
print("2. WEEKLY")
print("3. MONTHLY")
time_series_choice = int(input("Choice: "))
if time_series_choice == 1:
    time_series = "TIME_SERIES_DAILY_ADJUSTED"
elif time_series_choice == 2:
    time_series = "TIME_SERIES_WEEKLY_ADJUSTED"
elif time_series_choice == 3:
    time_series = "TIME_SERIES_MONTHLY_ADJUSTED"
else:
    print("Error: invalid time series function.")
    exit()

# Prompt the user for the beginning and end dates
begin_date_str = input("Enter the beginning date in YYYY-MM-DD format: ")
end_date_str = input("Enter the end date in YYYY-MM-DD format: ")

# Convert the dates to datetime objects and ensure end date is not before begin date
begin_date = datetime.strptime(begin_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
if end_date < begin_date:
    print("Error: end date is before begin date.")
    exit()

# Build the API request URL
url = f"https://www.alphavantage.co/query?function={time_series}&symbol={symbol}&apikey=BMUKTX4OV4DHV7Y1"

# Send the API request and get the response
response = requests.get(url)

# Load the response data into a dictionary
data = json.loads(response.text)

# Get the time series data from the dictionary
if time_series == "TIME_SERIES_DAILY_ADJUSTED":
    time_series_key = "Daily Adjusted Time Series"
elif time_series == "TIME_SERIES_WEEKLY_ADJUSTED":
    time_series_key = "Weekly Adjusted Time Series"
elif time_series == "TIME_SERIES_MONTHLY_ADJUSTED":
    time_series_key = "Monthly Adjusted Time Series"
else:
    print("Error: invalid time series function.")
    exit()

time_series_data = data[time_series_key]

# Extract the data for the selected date range
selected_data = {}
selected_open_data = {}
selected_high_data = {}
selected_low_data = {}
selected_close_data = {}
for date_str, values in time_series_data.items():
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if date >= begin_date and date <= end_date:
        selected_data[date_str] = float(values["4. close"])
        selected_open_data[date_str] = float(values["1. open"])
        selected_high_data[date_str] = float(values["2. high"])
        selected_low_data[date_str] = float(values["3. low"])
        selected_close_data[date_str] = float(values["4. close"])

# Create a chart based on user selection
if chart_type == "line":
    chart = pygal.Line(x_label_rotation=20)
elif chart_type == "bar":
    chart = pygal.Bar(x_label_rotation=20)
else:
    print("Error: invalid chart type.")
    exit()

# Add the data to the chart
chart.x_labels = selected_data.keys()
chart.add("Close", selected_data.values())
chart.add("Open", selected_open_data.values())
chart.add("High", selected_high_data.values())
chart.add("Low", selected_low_data.values())

# Set the chart title
chart_title = f"Stock data for {symbol}: {begin_date_str} to {end_date_str}"
chart.title = chart_title

# Render the chart to an SVG file
chart.render_to_file("chart.svg")

# Use lxml to open the rendered chart in the user's default browser
svg = etree.parse('chart.svg')
xml_string = etree.tostring(svg)
with open('chart.html', 'w') as f:
    f.write('<html><body>{}</body></html>'.format(xml_string.decode('utf-8')))
webbrowser.open('chart.html')
