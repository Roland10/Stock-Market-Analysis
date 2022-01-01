import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots


tesla = yf.Ticker('TSLA')

tesla_data = tesla.history(period='max')

tesla_data.reset_index(inplace=True)

tesla_data.head()

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

html_data = requests.get(url).text

soup = BeautifulSoup(html_data,"html.parser")
soup.find_all('title')

new = soup.find_all('tbody')

tesla_revenue = pd.DataFrame(columns=['Date','Revenue'])

for i in new[1].find_all('tr'):
    col = i.find_all('td')
    if (col != []):
        date = col[0].text
        revenue = col[1].text.replace("$","").replace(",","")
        tesla_revenue = tesla_revenue.append({"Date":date,"Revenue":revenue},ignore_index=True)

tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail()

def make_graph(stock_data,stock_revenue,stock):

    fig=make_subplots(rows=2,cols=1,shared_xaxes=True, subplot_titles=("Historical Share Price","Historical Revenue Price"), vertical_spacing=0.3)

    fig.add_trace(
    go.Scatter(x=stock_data.Date, y=stock_data.Close),row=1,col=1

)
    fig.add_trace(
    go.Scatter(x=stock_revenue.Date, y=stock_revenue.Revenue.astype("float")), row=2,col=1

)


    fig.update_yaxes(title_text="Price ($US)", row=1,col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Revenue($US Millions)", row=2,col=1)

    fig.update_layout(showlegend=False ,height=900, xaxis_rangeslider_visible=True)

    fig.show()

print(make_graph(tesla_data,tesla_revenue,'tesla'))
