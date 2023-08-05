# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:30:27 2018

@author: yili.peng
"""
import numpy as np
import pandas as pd
from joblib import Parallel,delayed

def zscore_df(price_df,pair_lst,halflife):
    '''
    pair_list: ['s1|s2','s1|s3','s2|s4',..]
    
    '''
    pair_df=pd.DataFrame([p.split('|') for p in pair_lst],columns=['t1','t2'])
    pair_df=pair_df.loc[pair_df['t1'].isin(price_df.columns)&pair_df['t2'].isin(price_df.columns)]
    ratio=pd.DataFrame(
            price_df[pair_df['t1']].values/price_df[pair_df['t2']].values
            ,index=price_df.index
            ,columns=pair_df.iloc[:,0].str.cat(pair_df.iloc[:,1],'|').tolist()
            )
    re=ratio.ewm(halflife=halflife,min_periods=halflife)
    zscore=ratio.sub(re.mean()).div(re.std())
    return ratio,zscore

def zscore_log_df(price_df,pair_lst,halflife):
    '''
    pair_list: ['s1|s2','s1|s3','s2|s4',..]
    
    '''
    pair_df=pd.DataFrame([p.split('|') for p in pair_lst],columns=['t1','t2'])
    pair_df=pair_df.loc[pair_df['t1'].isin(price_df.columns)&pair_df['t2'].isin(price_df.columns)]
    ratio=pd.DataFrame(
            np.log(price_df[pair_df['t1']].values/price_df[pair_df['t2']].values)
            ,index=price_df.index
            ,columns=pair_df.iloc[:,0].str.cat(pair_df.iloc[:,1],'|').tolist()
            )
    re=ratio.ewm(halflife=halflife,min_periods=halflife)
    zscore=ratio.sub(re.mean()).div(re.std())
    return ratio,zscore

def zscore_w(price_df,pair_lst,window):
    pair_df=pd.DataFrame([p.split('|') for p in pair_lst],columns=['t1','t2'])
    pair_df=pair_df.loc[pair_df['t1'].isin(price_df.columns)&pair_df['t2'].isin(price_df.columns)]
    ratio=pd.DataFrame(
            price_df[pair_df['t1']].values/price_df[pair_df['t2']].values
            ,index=price_df.index
            ,columns=pair_df.iloc[:,0].str.cat(pair_df.iloc[:,1],'|').tolist()
            )
    re=ratio.rolling(window)
    zscore=ratio.sub(re.mean()).div(re.std())
    return ratio,zscore

def zscore_log_w(price_df,pair_lst,window):
    '''
    pair_list: ['s1|s2','s1|s3','s2|s4',..]
    '''
    pair_df=pd.DataFrame([p.split('|') for p in pair_lst],columns=['t1','t2'])
    pair_df=pair_df.loc[pair_df['t1'].isin(price_df.columns)&pair_df['t2'].isin(price_df.columns)]
    ratio=pd.DataFrame(
            np.log(price_df[pair_df['t1']].values/price_df[pair_df['t2']].values)
            ,index=price_df.index
            ,columns=pair_df.iloc[:,0].str.cat(pair_df.iloc[:,1],'|').tolist()
            )
    re=ratio.rolling(window)
    zscore=ratio.sub(re.mean()).div(re.std())
    return ratio,zscore


def sig(zscore,k0=0,k1=1,k2=2):
    '''
    z: df
    k0,k1,k2: series/float/int
    
    sig:
        0 or nan or other number: hold still
        1: long
        2: close long position
        3: close long and open short
        -1: short
        -2: close short position
        -3: close short and open long 
        note: short means short first and long second, long means long first and short second, both with ratio (1,ratio)
        
    '''
    pairs_tmp=zscore.columns
    k0=(pd.Series(k0,index=pairs_tmp) if type(k0) in (float,int) else k0)
    k1=(pd.Series(k1,index=pairs_tmp) if type(k1) in (float,int) else k1)
    k2=(pd.Series(k2,index=pairs_tmp) if type(k2) in (float,int) else k2)
    pairs_left=list(set(k0.index) & set(k1.index) & set(k2.index) & set(pairs_tmp))
    
    zscore=zscore[pairs_left]
    k0=k0.loc[pairs_left]
    k1=k1.loc[pairs_left]
    k2=k2.loc[pairs_left]
    
    sell_return_signal=zscore.ge(k0).astype(int).diff().eq(-1)
    buy_return_signal=zscore.le(-k0).astype(int).diff().eq(-1)
    sell_force_out_signal=zscore.ge(k2).astype(int).diff().eq(1)
    buy_force_out_signal=zscore.le(-k2).astype(int).diff().eq(1)
    sell_signal=zscore.ge(k1).astype(int).diff().eq(1)
    buy_signal=zscore.le(-k1).astype(int).diff().eq(1)
    
    sig_df=pd.DataFrame(0,index=zscore.index,columns=zscore.columns)\
            .mask(buy_signal,1)\
            .mask(sell_return_signal,-2)\
            .mask(buy_force_out_signal,2)\
            .mask(sell_return_signal&buy_signal,-3)\
            .mask(sell_return_signal&buy_force_out_signal,-2)\
            .mask(sell_signal,-1)\
            .mask(buy_return_signal,2)\
            .mask(sell_force_out_signal,-2)\
            .mask(buy_return_signal&sell_signal,3)\
            .mask(buy_return_signal&sell_force_out_signal,2)
    return sig_df

def sig_tail(x,sign=2):
    '''
    return signal of each stationary period
    '''
    nonz = x[x!=0]
    if len(nonz) == 0:
        return 0
    elif nonz.iloc[-1] in (1,-3):
        return sign
    elif nonz.iloc[-1] in (-1,3):
        return -sign
    else:
        return 0

def split_by_na(ss,k):
    start=-1
    end=-1
    re=[]
    for i in range(ss.shape[0]):
        if ss.isna().iloc[i] and start==-1:
            continue
        elif ss.isna().iloc[i] or ((start!=-1) and (i == ss.shape[0]-1)):
            end=i
            re.append(ss.iloc[start:end+1])
            start=-1
            end=-1
        elif start==-1:
            start=i
    for r in re:
        r.iloc[-1]=sig_tail(r.iloc[:-1],k)
    if len(re)>0:
        return pd.concat(re).reindex(ss.index)
    else:
        return ss

def sig_cut_tail(sig_df,condition,n_jobs=-1,new_signal=4):
    '''
    sig_df: signal
    condition: statsionary condition filter, should be fitted in sig_df.where()
    '''
    sig_result_list=Parallel(n_jobs=n_jobs,verbose=10)(delayed(split_by_na)(col,new_signal) for key,col in sig_df.where(condition).items())
    sig_result=pd.concat(sig_result_list,axis=1)
    return sig_result