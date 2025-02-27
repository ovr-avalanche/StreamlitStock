
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import ff
from datetime import datetime, timedelta


stocklist = ff.get_stocklist(keys= True)
st.sidebar.title("Choose Stocks")

def test():
    st.write(st.session_state["multistock"])

#----- Select Stocks -----
st.session_state["multistock"] = ff.get_selected_stocks()
multistock = st.sidebar.multiselect("muliselect ", stocklist, key = "multistock", on_change=ff.store_selected_stocks)

#----- Render Title -----
ff.render_multistock_title(multistock)
bPlotSeperate = st.sidebar.checkbox("Plot each stock seperately")

#----- Date Input -----
date_input = st.sidebar.date_input("Start Date", value = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d'))
formated_date = date_input.strftime('%Y-%m-%d')


#----- Plot Stocks -----
ff.render_plotly(bPlotSeperate, multistock, formated_date)


# ====== Add Stocks to json files ======  not sure i like the nested widgets
st.sidebar.title("Add a new stock")
st.sidebar.caption("This will permanently add a new stock to the list of stocks")
new_stock = st.sidebar.text_input("Enter the name of the new stock")
if new_stock != "":
    abreviation = st.sidebar.text_input("Enter the abreviation of the new stock")
    if abreviation != "":
        addstockbutton = st.sidebar.button("add stock")
        ff.add_stocks_to_json(new_stock, abreviation, addstockbutton)

# ====== remove Stocks ======
st.sidebar.title("remove stock")
st.sidebar.caption("This will permanently remove a stock from the list of stocks")
stocks_to_remove = st.sidebar.multiselect("select stocks to remove", stocklist, key = "remove_multiselect")
buttonval = st.sidebar.button("Remove selected stocks")
ff.remove_stocks(stocks_to_remove, buttonval)
st.sidebar.write(buttonval)