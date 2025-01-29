import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import json
import plotly.express as px


def render_multistock_title(multistock: list[str]):
    if len(multistock)==0:
        st.title("No Stocks Selected")
        return
    stockstring: str = ""
    for string in multistock:
        stockstring += string + ", "
    stockstring = stockstring[:-2] + " "
    st.title(stockstring + "Stocks")

def get_stocklist(keys = False, values = False):
    file_path = "stocks.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)    

    except FileNotFoundError:
        print("File not found")
        return
    if values == True:
        return data.values()
    if keys == True:
        return data.keys()


#def plot_stocks(bPlotInOne):
#    Stocklist = get_stocklist(keys = False, values = True)
#    fig, ax = plt.subplots()
#    open_closed = st.sidebar.selectbox("Select a column", ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
#    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
#    end_date = datetime.today().strftime('%Y-%m-%d')
#    
#    for stock in Stocklist:
#        stockticker = yf.Ticker(stock)
#
#        stockdata = stockticker.history(period="1d", start=start_date, end=end_date)  
#
#        ax.plot(stockdata[open_closed], label = stock)
#
#        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#        if(bPlotInOne == False):
#            st.pyplot(fig)
#           
#    st.pyplot(fig) # rework such tthat each stock is plotted allone
#    st.caption(start_date + " to " + end_date)

def render_plotly(bPlotSeperate: bool):
    Stocklist = get_stocklist(keys = False, values = True)
    fig, ax = plt.subplots()
    open_closed = st.sidebar.selectbox("Select a column", ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    st.caption(start_date + " to " + end_date)

    if bPlotSeperate == False:
        fig = px.line(title="Stocks")
        for stock in Stocklist:
            stockticker = yf.Ticker(stock)

            stockdata = stockticker.history(period="1d", start=start_date, end=end_date)
            fig.add_scatter(x=stockdata.index, y=stockdata[open_closed], name=stock)
        st.plotly_chart(fig)
    else:            
        for stock in Stocklist:
            stockticker = yf.Ticker(stock)

            stockdata = stockticker.history(period="1d", start=start_date, end=end_date)
            fig = px.line(stockdata, x=stockdata.index, y=open_closed, title=stock)
            st.plotly_chart(fig)
    


def add_stocks_to_json(new_stock: str, abreviation: str, buttonval: bool):
    if buttonval == False:
        return
        print("buttonval is false")
    file_path = "stocks.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)    

    except FileNotFoundError:
        print("File not found")
        return
    # add the new stock to the lists
    data[new_stock] = abreviation

    # save the new data
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    buttonval = False


def remove_stocks(stocks_to_remove: list[str], buttonval):
    if buttonval == False:
        return
    file_path = "stocks.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)    

    except FileNotFoundError:
        print("File not found")
        return
    # remove the stock from the list
    for stock_name in stocks_to_remove:
        data.pop(stock_name)

    # save the new data
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    st.session_state.buttonval = False
    #st.session_state.remove_multiselect = []



