# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:57:04 2018

@author: yili.peng
"""

from datetime import date,timedelta
import pandas as pd
from RNWS import write_df,detect_last_date
from time import strftime,localtime

def trading_times(w,length=180,text="TradingCalendar=HKEX"):
    '''
    get the last 180 trading date for HK stocks
    '''
    start_len=length
    times=[]
    today=date.today()
    while len(times)<length:
        start_len+=10
        sday=today-timedelta(start_len)
        t=w.tdays(sday, today, text)
        if t.Times[-1]==today:
            times=t.Times[:-1]
        else:
            times=t.Times
    return times[-length:]

def load_hist_price(tickers,times,w,text="TradingCalendar=HKEX"):
    '''
    load hist data
    '''
    hist_price=[]
    for dt in times:
        print('load %s'%dt.strftime('%Y%m%d'))
        result_dt=pd.DataFrame()
        lst=['close', 'adjfactor']
        for l in lst:
            print(l)
            w_load=w.wsd(tickers, l , dt, dt)
            if w_load.ErrorCode!=0:
                raise Exception('Wind Error')
            result_dt=pd.concat([result_dt,pd.Series(w_load.Data[0],index=w_load.Codes,name=l)],axis=1)
        hist_price.append(result_dt.eval('close*adjfactor').rename(int(dt.strftime('%Y%m%d'))))
    return pd.concat(hist_price,axis=1).T

def download_hist_price(tickers,times,path,w,pattern='price',**kwargs):
    '''
    download data up to yesterday
    '''
    last_dt=detect_last_date(path)
    lst=[(None if int(i.strftime('%Y%m%d'))<last_dt else i) for i in times]
    while True:
        try:
            lst.remove(None)
        except:
            break
    price=load_hist_price(tickers,lst,w,**kwargs)
    write_df(price,path,pattern)

def load_instant_price(tickers,w,adj=None,text="TradingCalendar=HKEX"):
    '''
    load price data instantly
    '''    
    t=strftime('%Y-%m-%d %H:%M:%S',localtime())
    if len(tickers)==1 and tickers[0]=='':
        return pd.Series(name=date.today().strftime('%Y%m%d')),pd.Series(name=date.today().strftime('%Y%m%d')),t
    w_load=w.wsq(tickers,'rt_last', text)
    if (w_load.ErrorCode!=0):
        raise Exception('Wind Error')
    today=date.today()
    if adj is None:
        w_load2=w.wsd(tickers, 'adjfactor' , today, today,text)
        if (w_load2.ErrorCode!=0):
            raise Exception('Wind Error')
        adjfactor=pd.Series(w_load2.Data[0],index=w_load2.Codes)
    else:
        adjfactor=adj.reindex(w_load.Codes)
    rt_last=pd.Series(w_load.Data[0],w_load.Codes)        
    return rt_last.rename(date.today().strftime('%Y%m%d')),adjfactor.rename(date.today().strftime('%Y%m%d')),t