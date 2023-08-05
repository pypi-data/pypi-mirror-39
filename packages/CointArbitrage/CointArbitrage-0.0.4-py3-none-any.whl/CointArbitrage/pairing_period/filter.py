# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:46:24 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np
from joblib import Parallel,delayed
from .CointTest import coint

def filter_tickers(df,na_rate=0.1,thresh=20):
    '''
    filter tickers by applying threshold to na values of price
    '''
    chosen_columns=df.columns[(df.isna().mean()<na_rate)]
    chosen2=chosen_columns[~df[chosen_columns].pct_change().eq(0).rolling(thresh).sum().eq(thresh).any()]
    return df[chosen2].ffill()


def filter_pval(price,pairs,thresh=0.1,n_jobs=-1,multi=True):
    '''
    filter pairs by stationarity
    '''
    if multi:
        pval=Parallel(n_jobs=n_jobs,verbose=40)(delayed(coint)((price[p.split('|')[0]],price[p.split('|')[1]])) for p in pairs)
    else:
        pval=[coint(price[p.split('|')[0]],price[p.split('|')[1]]) for p in pairs]
    p=pd.DataFrame(pval,index=pairs,columns=('stats','pval'))
    return list(p.index[p.pval.le(thresh)])

def ticker_pairs(tickers,pairs):
    # pairs filtered by tickers
    left=list(pairs)
    for p in pairs:
        for t in p.split('|'):
            if t not in tickers:
                left.remove(p)
                break
    # tickers from pairs
    t=pd.Series(pairs).str.split('|',expand=True).unstack().drop_duplicates().tolist()
    return t,left

def filter_price(price,pairs,thresh=0.1):
    '''
    filter price according to pairs
    '''
    chosen_stocks=price.columns[price.diff().eq(0).mean().le(thresh)]
    new_tickers,new_pairs=ticker_pairs(chosen_stocks,pairs)    
    return price[chosen_stocks],np.array(pairs)[pd.Series(pairs).str.split('|',expand=True).isin(chosen_stocks).all(axis=1)]
