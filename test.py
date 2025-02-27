#import pandas as pd
#import numpy as np
#import yfinance as yf
#import matplotlib.pyplot as plt 
#import json
#from datetime import datetime, timedelta
#import plotly.express as px


import streamlit as st

with st.sidebar.form(key="user_form"):
	name = st.text_input("Enter Name:")
	age = st.number_input("Enter Age:")
	st.form_submit_button()
	
st.write(f"""
    # Name: {name}
    # Age: {int(age)}
    
""")