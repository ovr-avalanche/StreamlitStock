
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import ff


stocklist = ff.get_stocklist(keys= True)

multistock = st.sidebar.multiselect("Select mulstiple stocks", stocklist)

ff.render_multistock_title(multistock)
bPlotSeperate = st.sidebar.checkbox("Plot each stock seperately")
ff.render_plotly(bPlotSeperate)


# ====== Add Stocks to json files ======
st.sidebar.title("Add a new stock")
new_stock = st.sidebar.text_input("Enter the name of the new stock")
abreviation = st.sidebar.text_input("Enter the abreviation of the new stock")
addstockbutton = st.sidebar.button("add stock")
ff.add_stocks_to_json(new_stock, abreviation, addstockbutton)

# ====== remove Stocks ======
st.sidebar.title("remove stock")
stocks_to_remove = st.sidebar.multiselect("select stocks to remove", stocklist, key = "remove_multiselect")
buttonval = st.sidebar.button("Remove selected stocks")
ff.remove_stocks(stocks_to_remove, buttonval)
st.sidebar.write(buttonval)