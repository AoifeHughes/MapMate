from .mm_utility import process_df
import pandas as pd 
import numpy as np
import pycountry

def prepare_data(loc, data_col, cname_cols, long_col='Longitude', lat_col='Latitude' , nrows=None, col_mods=[]): 
    """
        Prepares a data file for use in this library 
        
        loc = data location on disk, or df
        data_col = the value to map
        cname_cols = country/groupby columns

        optionals:
        long/lat_col is the positional data columns
        nrows allows for limiting number of rows read
        col_mods provides f(x) style modification of the dataframe and is done after reading data
            these fs should not return anything


    """
    if type(loc) == str:
        df = pd.read_csv(loc, nrows=nrows)
    else:
        df = loc[:nrows] if nrows is not None else loc
    df = df[df[data_col].notna()]
    for f in col_mods:
        f(df)
        
    # this is on the user to monitor
    # poss double memory waste on using 2x dfs 
    tdf = process_df(df, cname_cols, lat_col, long_col)
    keys = [list(pycountry.countries)[i].alpha_3 for i in range(len(pycountry.countries))]
    names = [list(pycountry.countries)[i].name for i in range(len(pycountry.countries))]
    conv = { v:k for k,v in zip(keys,names) }
    def match_name(x):
        try:
            return conv[x]
        except KeyError as e:
            for  n in names:
                if x in n:
                    return conv[n]
            return 'N/A'
    tdf['codes'] = tdf.apply(lambda x: match_name(x['Country']), axis=1)
    return tdf