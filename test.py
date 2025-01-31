#import pandas as pd
#import numpy as np
#import yfinance as yf
#import matplotlib.pyplot as plt 
#import json
#from datetime import datetime, timedelta
#import plotly.express as px


import streamlit as st

def store():
   with open("selected.txt", "w") as file:
            file.writelines("\n".join(st.session_state["ms"]))

def get_selected_stocks():
    with open("selected.txt", "r") as file:
        my_list = file.read().splitlines()
    return my_list

st.session_state["ms"] = get_selected_stocks()

st.sidebar.multiselect("multitest", ["test1", "test2", "test3", "test4", "test5"], key = "ms", on_change=store)

st.write(st.session_state)