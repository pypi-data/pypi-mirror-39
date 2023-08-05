# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 09:55:18 2018

@author: yili.peng
"""
from itertools import combinations
from statsmodels.tsa.tsatools import add_trend
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.adfvalues import mackinnonp
import pandas as pd
from joblib import Parallel,delayed

def coint(X):
    y0_tmp,y1_tmp=X[0],X[1]
    y0=y0_tmp[~(pd.isna(y0_tmp)|pd.isna(y1_tmp))]
    y1=y1_tmp[~(pd.isna(y0_tmp)|pd.isna(y1_tmp))]
    xx = add_trend(y1, trend='c', prepend=False)
    try:
        res_co2 = OLS(y0, xx).fit()
        res_adf = adfuller(res_co2.resid,regression='nc')
        pval_asy = mackinnonp(res_adf[0], regression='c', N=2)
        return res_adf[0],pval_asy
    except:
        return np.nan,np.nan

def find_pair(price,mul=True,n_jobs=1,**kwargs):
    if not mul:
        r=[[comb[0],comb[1],coint((price[comb[0]].values,price[comb[1]].values))[1]] for comb in combinations(price.columns,2)]
    else:
        print('\rpool start',end='\r')
        col_lst=[list(comb) for comb in combinations(price.columns,2)]
        rs=Parallel(n_jobs=n_jobs,**kwargs)(delayed(coint)((price[comb[0]].values,price[comb[1]].values)) for comb in col_lst)
        r=[[col_lst[i][0],col_lst[i][1],rs[i][1]] for i in range(len(col_lst))]
    return pd.DataFrame(r,columns=['ticker1','ticker2','p_value'])
