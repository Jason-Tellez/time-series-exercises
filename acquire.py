import pandas as pd
import numpy as np
import requests


def get_retail_df(url, target):
    """
    Function takes in a url and target data you wish to acquire, iterates through the pages,
    concats all pages of data to a dataframe and returns that dataframe.
    """
    
    # passes given url using get
    response = requests.get(url)
    # Reads json object as data structure using .json
    data = response.json()
    # turns part of structure into a dataframe
    df = pd.DataFrame(data["payload"][target])
    
    # Loop that iterates through the other pages, if any, of the json object and concats into a single dataframe
    if data['payload']['max_page'] > 1:
        for i in range(2, data["payload"]["max_page"] + 1):
            response = requests.get(url + "?page=" + str(i))
            data = response.json()
            df = pd.concat( [ df, pd.DataFrame( data["payload"][target] ) ] )
            
    return df



def merge_dfs(left_df, left_key, right_df, right_key, join_type):
    """
    Function takes two dataframes, two keys to join on, and a join type and return a merged dataframe using pd.merge.
    """
    
    df = left_df.merge(right_df,
                      how=join_type,
                      left_on=left_key,
                      right_on=right_key
                      )
    return df



def read_csv(url):
    """
    Function reads a csv and returns a dataframe.
    """
    df = pd.read_csv(url)
    return df


def get_merged_retail():
    df1 = get_retail_df("https://python.zgulde.net/api/v1/items", "items")
    df2 = get_retail_df("https://python.zgulde.net/api/v1/sales", "sales")
    df3 = get_retail_df("https://python.zgulde.net/api/v1/stores", "stores")
    
    first_merge = merge_dfs(df1, "item_id", df2, "item", "outer")
    df = merge_dfs(first_merge, "store", df3, "store_id", "outer")

    return df