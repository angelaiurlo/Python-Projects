import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

#create an object for AAPL (Apple)
apple = yf.Ticker("AAPL")

# get historical market data
apple_data=apple.history(period="max")

apple_data.reset_index(inplace=True)

#create an object for AMD (Advanced Micro Devices)
amd=yf.Ticker("AMD")
amd_data=amd.history(period="max")

amd_data.reset_index(inplace=True)

#Extracting Netflix stock data using a Web Scraping BeautifulSoup
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data=requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')
netflix_df = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text

    # Finally we append the data of each row to the table
    netflix_df = pd.concat([netflix_df,pd.DataFrame({"Date":[date], "Open":[Open], "High":[high], "Low":[low], "Close":[close], "Adj Close":[adj_close], "Volume":[volume]})], ignore_index=True)

#Extracting Amazon Data using Pandas
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html"
read_html_pandas_data = pd.read_html(url)
netflix_df = read_html_pandas_data[0]
netflix_df.head()
