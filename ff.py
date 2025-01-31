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
    
    title_string: str = ""
    for string in multistock:
        title_string += string + ", "
    title_string = title_string[:-2] + " "
    st.title(title_string + "Stocks")

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

def get_abreviation(stock_name: str):
    file_path = "stocks.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)    

    except FileNotFoundError:
        print("File not found")
        return
    return data[stock_name]


def render_plotly(bPlotSeperate: bool, multistock: list[str]):
    fig, ax = plt.subplots()
    open_closed = st.sidebar.selectbox("Select a column", ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    #end_date = yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d') # get yesterdays date
    st.caption(start_date + " to " + end_date)

    if bPlotSeperate == False:
        fig = px.line()
        for stock in multistock:
            stock = get_abreviation(stock)
            stockticker = yf.Ticker(stock)
            stockdata = stockticker.history(period="1d", start=start_date, end=end_date)
            fig.add_scatter(x=stockdata.index, y=stockdata[open_closed], name=stock)
        st.plotly_chart(fig)
    else:
        col1, col2 = st.columns(2)
        stock_counter = 1            
        for stock in multistock:
            stock_counter += 1
            stock = get_abreviation(stock)
            stockticker = yf.Ticker(stock)

            stockdata = stockticker.history(period="1d", start=start_date, end=end_date)
            fig = px.line(stockdata, x=stockdata.index, y=open_closed, title=stock)
            if len(multistock) < 2:
                st.plotly_chart(fig)
                return
            if stock_counter % 2 == 0:
                col1.plotly_chart(fig)
            else:
                col2.plotly_chart(fig)
    
    
def store_selected_stocks():
    """ stores a list in the selected.txt file, elements should be full names of stocks """
    with open("selected.txt", "w") as file:
        file.writelines("\n".join(st.session_state["multistock"]))

        
def get_selected_stocks():
    """ returns a list from the selected.txt file """

    with open("selected.txt", "r") as file:
        my_list = file.read().splitlines()
    return my_list

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



