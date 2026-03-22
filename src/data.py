import pandas as pd
import yfinance as yf
import os
from datetime import datetime, timedelta

def get_stock_data(stock_name: str,
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d'),
    end_date = datetime.today().strftime('%Y-%m-%d')) -> pd.DataFrame:

    """returns a dataframe with the stock data for the given stock name, looks in data folder for the parquet file, 
    if it doesn't find it, it will download the data from yfinance and save it as a parquet file in the data folder. Daily interval data.
    
    Parameters
    -----------
    stock_name: str
        the name of the stock to get the data for (not the abreviation).
    start_date: str
        the start date for the data in the format 'YYYY-MM-DD', default is one year ago.
    end_date: str
        the end date for the data in the format 'YYYY-MM-DD', default is today.

    Returns
    -------
    pd.DataFrame: a dataframe with the stock data for the given stock name and date range 
    """
    
    stock_name :str = stock_name.lower()
    parque_exists :bool = _parque_exists(stock_name)

    if parque_exists and _parque_has_interval(stock_name, start_date, end_date):
        df = pd.read_parquet(r"data/" + stock_name + ".parquet")
        return df[(df.index >= start_date) & (df.index <= end_date)]
    
    elif parque_exists: # parque file exists but does not have the required date range
        print("time range does not exist in parquet file")
        return _update_parquet_file(stock_name, start_date, end_date)

    else:# parquete file does not exist
        print(f"parquet file for {stock_name} does not exist")
        df = _download_stock_data(stock_name, start_date, end_date)
        df.to_parquet(r"data/" + stock_name + ".parquet")
        return df



##################################################################################################

def _parque_exists(stock_name: str) -> bool:
    """ checks if a parquet file for the given stock name exists in the data folder """
    return (r"data/" + stock_name + ".parquet") in [f"data/{file}" for file in os.listdir("data")]

def _parque_has_interval(stock_name: str, start_date: str, end_date: str) -> bool:
    """ checks if the given date range exists in the parquet file for the given stock name """
    df = pd.read_parquet(r"data/" + stock_name + ".parquet")
    return (start_date >= df.index.min().strftime('%Y-%m-%d')) and (end_date <= df.index.max().strftime('%Y-%m-%d'))


def _download_stock_data(stock_name: str, start_date: str, end_date: str)-> pd.DataFrame:
    """ downloads the missing data from yfinance and returns a DataFrame """
    stockticker = yf.Ticker(stock_name)
    stockdata = stockticker.history(period="1d", start=start_date, end=end_date)
    #stockdata.to_parquet(r"data/" + stock_name + ".parquet")
    return stockdata

def _update_parquet_file(stock_name: str, start_date: str, end_date: str):
    """ updates the parquet file for the given stock name with the missing data from yfinance 
    and returns a DataFrame with the complete data for the given date range """
    df_existing = pd.read_parquet(r"data/" + stock_name + ".parquet")
    existing_start_Date = df_existing.index.min().strftime('%Y-%m-%d')
    existing_end_date = df_existing.index.max().strftime('%Y-%m-%d')

    df_new_data = []
    if start_date < existing_start_Date:
        df_new_data.append(_download_stock_data(stock_name, start_date, existing_start_Date))
    if end_date > existing_end_date:
        df_new_data.append(_download_stock_data(stock_name, existing_end_date, end_date))
    
    df_new = pd.concat(df_new_data) if df_new_data else pd.DataFrame()
    df_new = df_new[~df_new.index.duplicated(keep="first")]
    df_new = df_new.sort_index()

    df_new.to_parquet(r"data/" + stock_name + ".parquet")
    return df_new

# -------------- TESTING --------------


print(pd.read_parquet(r"data/apple.parquet").head(5))

res = get_stock_data("Apple", "2023-01-02", "2025-01-04")

print(pd.read_parquet(r"data/apple.parquet").head(5))