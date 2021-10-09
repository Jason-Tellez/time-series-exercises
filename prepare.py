import pandas as pd
import numpy as np
import requests

from datetime import timedelta, datetime

import seaborn as sns
import matplotlib.pyplot as plt

# no yelling in the library
import warnings
warnings.filterwarnings("ignore")

import acquire as a

def prep_sales(df, date_index):
    df = df.assign(date = pd.to_datetime(df[date_index])).\
    assign(df.set_index(date_index).sort_index())
    
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    
    return df


def prep_germ(df, date_index):
    df.Date= pd.to_datetime(df.Date)
    df = df.set_index('Date').sort_index()
    df['year'] = df.index.year
    df['month'] = df.index.month_name()
    df.Wind.fillna(0, inplace=True)
    df.Solar.fillna(0, inplace=True)
    df['Wind+Solar'] = df.Wind + df.Solar
              
    return df