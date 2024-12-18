import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Use yfinance library to extract AMD (Advanced Micro Devices) Stock data
amd=yf.Ticker("AMD")
amd_data=amd.history(period="max")
amd_data.reset_index(inplace=True)

#Use BeautifulSoup to Extract Tesla Revenue Data
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text
soup=BeautifulSoup(html_data,'html.parser')
tesla_revenue=pd.DataFrame(columns=['Date','Revenue'])

for x in soup.find_all('tbody')[1].find_all('tr'):
  col=x.find_all('td')
  data=col[0].text
  revenue=col[1].text
  tesla_revenue=pd.concat([tesla_revenue,pd.DataFrame({'Date':[data],'Revenue':[revenue]})],ignore_index=True)
    
#remove comma and dollar signs
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',',"")
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace('$',"")

#remove null or empty string
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Use Pandas to extract GameStop stock data
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
gme_tables=pd.read_html(url)
gme_revenue_table=gme_tables[1]
gme_revenue_table.rename(columns={'GameStop Quarterly Revenue (Millions of US $)':'Date','GameStop Quarterly Revenue (Millions of US $).1':'Revenue'},inplace=True)

#remove comma and dollar signs
gme_revenue['Revenue']=gme_revenue['Revenue'].str.replace(',','')
gme_revenue['Revenue']=gme_revenue['Revenue'].str.replace('$','')

#remove null or empty string
gme_revenue.dropna(inplace=True)
gme_revenue=gme_revenue[gme_revenue['Revenue']!=""]

#Create a dashboard
#function to plot the revenue data
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    
amd_data.plot(x="Date", y="Open", title="AMD Stock Price")
make_graph(tesla_data,tesla_revenue,"Tesla Revenue")
make_graph(gme_data,gme_revenue,"GameStop Revenue")
