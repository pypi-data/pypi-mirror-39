# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:49:52 2018

@author: yili.peng
"""
import numpy as np
from time import sleep
import pandas as pd
import os
from .load_wind import load_instant_price
from ..pairing_period import filter_price,coint,filter_pval
from ..trading_period import zscore_w,zscore_log_w,sig
from .position_with_constrain import match
from .tail import tail_pairs
from functools import wraps

def init_log(path):
    if os.path.exists(path):
        print('file already exists')
    else:
        with open(path,'w') as f:
            f.write('pair,open_date,open_time,long,long_price,long_current_price,long_lot_size,long_lot_count,short,short_price,short_current_price,short_lot_size,short_lot_count,current_date,current_time,close_mark,abs_return,return,long_adj_price,long_volume,short_adj_price,short_volume,volume_delta,zscore')

def sleep_by_sec(sleep_time):
    for i in range(sleep_time):
        print('\rsleep %ds'%(sleep_time-i),end='\r')
        sleep(1)
    print('')

def check_time_hk(time_now):
    '''
    0: trading time
    1: short break / before trading
    2: after trading 
    3: last 10min of trading
    '''
    if ((int(time_now[-8:-6])>=12) and (int(time_now[-8:-6])<13)) or ((int(time_now[-8:-6])==9) and (int(time_now[-5:-3])<=30)) or (int(time_now[-8:-6])<9) :
        return 1
    elif int(time_now[-8:-6])>=16:
        return 2
    elif int(time_now[-8:-6])==15 and int(time_now[-5:-3])>=50:
        return 3
    else:
        return 0

def time_sleep(sign={0:1800,1:900,2:'break',3:'break'}):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if 'break' not in sign.values():
                print('To stop sleep must have at leat a sign `break` to stop loop')
                return func(*args,**kwargs)
            log=func(*args,**kwargs)
            if log not in sign.keys():
                print('Return of %s is not in sign.keys()'%func.__name__)
                return log
            while sign[log]!='break':
                sleep_by_sec(sign[log])
                log=func(*args,**kwargs)
            print('break')
            return log
        return wrapper
    return decorator

def find_new_hk(log_path,hist_price,pairs,tickers,zs_window,w,ls,hist_log=None,adjfactor=None,potential_path=None,potential_k=1.8,zs_log=False,k0=1,k1=2,k2=4,match_max=50000):
    '''
    log_path: path to store log file. log file should contains headers: pair,open_date,open_time,long,long_price,long_current_price,long_lot_size,long_lot_count,short,short_price,short_current_price,short_lot_size,short_lot_count,current_date,current_time,close_mark,abs_return,return,long_adj_price,long_volume,short_adj_price,short_volume,volume_delta
    hist_price: historical price with specific length of trading times.
    pairs: candidate pairs.
    tickers: cadidate stock tickers.
    zs_window: window to calculate zscore.
    w: from WindPy import w
    ls: lotsize and shortability, dataframe with index as tickers, columns as ['shortable','lotsize'] and values like [(0,1000),(1,500),...]
    adjfactor: pre load adjfactor to download
    hist_log: log from back test (position.log). This is used to plot historical performance.(optional) 
    potential_path: path of potential pairs.
    potential_k: potential pairs are defined as pairs with absulute zscore in between potential_k and k2 
    zs_log: whether to use log zscore instead of normal zscore. This should be the same as in back test.
    k0: thresh to close position
    k1: thresh to open position
    k2: thresh to close out position
    match_max: max dollars to trade one stock. Max dollars of a pair is roughly doubled by this number.
    
    return
        0,1,2,3 as in check_time_hk returns
    '''
    last_pos=pd.read_csv(log_path)
    live_pair=last_pos.pair.loc[last_pos.close_mark.isna()].tolist()    
    
    # renewal price,adj,zscore
    instant_price,adjfactor,time_now=load_instant_price(tickers,w,adj=adjfactor)
    print('\n\n\n\n',time_now) 
    ft=check_time_hk(time_now)
    if ft != 0:
        return ft
    elif instant_price.shape[0]==0:
        return ft
        
    all_price=hist_price.append(instant_price.mul(adjfactor)).iloc[1:]
    # filter anomaly prices
    pr1,pairs1=filter_price(all_price.iloc[-zs_window:],pairs)        
    # zscore
    if not zs_log:
        ratio,zs=zscore_w(all_price,pairs1,window=zs_window)
    else:
        ratio,zs=zscore_log_w(all_price,pairs1,window=zs_window)
    # signal
    sg_last=sig(zscore=zs.iloc[-zs_window:],k0=k0,k1=k1,k2=k2).iloc[-1]
    # potential trade list
    to_trade_list=list(sg_last.index[(sg_last==1)|(sg_last==-3)|(sg_last==-1)|(sg_last==3)])    
    print('pairs to trade:',len(to_trade_list))    
    to_print=[]    
    for p in set(to_trade_list).difference(set(live_pair)):        
        if zs.iloc[-1].loc[p]>k1:
            short,long=p.split('|')
        elif zs.iloc[-1].loc[p]<-k1:
            long,short=p.split('|')
        else:
            continue        
        if ls.shortable.loc[short]==0:
            # not shortable            
            continue
        else:
            stats,p_val=coint((all_price[long],all_price[short]))
            if p_val>0.1:
                continue        
        instant_long,instant_short=instant_price.loc[long],instant_price.loc[short]
        price_long,price_short=pr1[long].iloc[-1],pr1[short].iloc[-1]
        lot_size_long,lot_size_short=ls.lotsize.loc[long],ls.lotsize.loc[short]
        lot_long,lot_short=match(instant_long, instant_short, lot_size_long, lot_size_short,m=match_max)    
        to_print.append([p]+time_now.split(' ')+\
                        ([long,# long'
                          instant_long.round(2), # 'long_price'
                          np.nan, #'long_current_price',
                          lot_size_long, #'long_lot_size'
                          lot_long, #'long_lot_count'                
                          short, 
                          instant_short.round(2), 
                          np.nan,
                          lot_size_short, 
                          lot_short, 
                          None,#'current_date'
                          None,#'current_time'
                          None,#'close_mark'
                          None,#'abs_return'
                          None,#'return'
                          price_long,#'long_adj_price'
                          lot_long*lot_size_long*instant_long,#'long_volume'
                          price_short,
                          lot_short*lot_size_short*instant_short,
                          lot_long*lot_size_long*instant_long - lot_short*lot_size_short*instant_short,
                          zs[p].iloc[-1] #zscore
                          ]))   
        if hist_log is not None:
            tail_pairs(p,pr1,zs.reindex(pr1.index),log=hist_log,time=time_now)
        print('price:\n',pr1[p.split('|')].iloc[-1])
        print('zscore:\n',zs[p].iloc[-1])
    new_pos=pd.concat([last_pos,pd.DataFrame(to_print,columns=last_pos.columns)],axis=0)
    new_pos.to_csv(log_path,float_format='%.2f',index=False,columns=last_pos.columns)
    print('output log')
    # potential
    # signal
    if not (potential_path is None):
        last_zs=zs.iloc[-1]
        po_to_trade_list= last_zs.index[last_zs.abs().ge(potential_k) & last_zs.abs().le(k1)]
        to_print=[]
        print('potential pairs to trade:',len(po_to_trade_list))
        for p in po_to_trade_list:
            if last_zs.loc[p]>potential_k:
                short,long=p.split('|')
            elif last_zs.loc[p]<-potential_k:
                long,short=p.split('|')
            else:
                continue            
            if ls.shortable.loc[short]==0:
                # not shortable            
                continue
            else:
                instant_long,instant_short=instant_price.loc[long],instant_price.loc[short]
                lot_size_long,lot_size_short=ls.lotsize.loc[long],ls.lotsize.loc[short]
                lot_long,lot_short=match(instant_long, instant_short, lot_size_long, lot_size_short,m=match_max)
                zs=last_zs.loc[p]
                to_print.append([time_now,long,lot_size_long,lot_long,short,lot_size_short,lot_short,zs,p])                
        pd.DataFrame(to_print,columns=['time','long','long_lotsize','long_lot','short','short_lotsize','short_lot','zscore','mark'])\
                .to_csv(potential_path,float_format='%.2f',index=False)        
        print('output potential')
    return 0

def potential(potential_path,tickers,pairs,hist_price,w,ls,zs_window=20,zs_log=False,k1=2,potential_k=1.8,match_max=50000):
    instant_price,adjfactor,time_now=load_instant_price(tickers,w,adj=None)
    print('\n\n\n\n',time_now)
    all_price=hist_price.append(instant_price.mul(adjfactor)).iloc[1:]
    pr1,pairs1=filter_price(all_price.iloc[-zs_window:],pairs)   
    # zscore
    if not zs_log:
        ratio,zs=zscore_w(all_price,pairs1,window=zs_window)
    else:
        ratio,zs=zscore_log_w(all_price,pairs1,window=zs_window)
    last_zs=zs.iloc[-1]
    po_to_trade_list= last_zs.index[last_zs.abs().ge(potential_k) & last_zs.abs().le(k1)]
    to_print=[]
    print('potential pairs to trade:',len(po_to_trade_list))
    for p in po_to_trade_list:
        if last_zs.loc[p]>potential_k:
            short,long=p.split('|')
        elif last_zs.loc[p]<-potential_k:
            long,short=p.split('|')
        else:
            continue            
        if ls.shortable.loc[short]==0:
            # not shortable            
            continue
        else:
            instant_long,instant_short=instant_price.loc[long],instant_price.loc[short]
            lot_size_long,lot_size_short=ls.lotsize.loc[long],ls.lotsize.loc[short]
            lot_long,lot_short=match(instant_long, instant_short, lot_size_long, lot_size_short,m=match_max)
            zs=last_zs.loc[p]
            to_print.append([time_now,long,lot_size_long,lot_long,short,lot_size_short,lot_short,zs,p])                
    pd.DataFrame(to_print,columns=['time','long','long_lotsize','long_lot','short','short_lotsize','short_lot','zscore','mark'])\
            .to_csv(potential_path,float_format='%.2f',index=False)        
    print('output potential')

    
    
def refresh_hk(log_path,hist_price,w,hist_log=None,k0=1,k2=4,plot_mark=None,potential_path=None,zs_log=False,zs_window=20):
    '''
    log_path: path to store log file. log file should contains headers: pair,open_date,open_time,long,long_price,long_current_price,long_lot_size,long_lot_count,short,short_price,short_current_price,short_lot_size,short_lot_count,current_date,current_time,close_mark,abs_return,return,long_adj_price,long_volume,short_adj_price,short_volume,volume_delta
    hist_price: historical price with specific length of trading times.
    w: from WindPy import w
    zs_window: window to calculate zscore.
    zs_log: whether to use log zscore instead of normal zscore. This should be the same as in back test.
    hist_log: log from back test (position.log). This is used to plot historical performance.(optional) 
    potential_path: path of potential pairs.   
    k0: thresh to close position
    k2: thresh to close out position
    
    return
        0,1,2,3 as in check_time_hk returns
    '''
    # renewal within one day
    last_pos=pd.read_csv(log_path)
    
    # find pairs
    pairs=last_pos.pair.loc[last_pos.close_mark.isna()].tolist()
    tickers=list(np.unique('|'.join(pairs).split('|')))
    
    instant_price,adjfactor,time_now=load_instant_price(tickers,w,adj=None)
    print('\n\n\n\n',time_now)
    ft=check_time_hk(time_now)
    if ft !=0:
        return ft  
    elif instant_price.shape[0]==0:
        return ft
        
    all_price=hist_price[tickers].append(instant_price.mul(adjfactor)).iloc[1:]
    # zscore
    if not zs_log:
        ratio,zs=zscore_w(all_price,pairs,window=zs_window)
    else:
        ratio,zs=zscore_log_w(all_price,pairs,window=zs_window)
    last_price,last_zs=all_price.iloc[-1],zs.iloc[-1]
    renewal_pos=pd.DataFrame()
    for inx in last_pos.index:
        if last_pos['close_mark'].isna().loc[inx]:
            # not closed yet
            s=last_pos.loc[inx]
            s.current_date,s.current_time=time_now.split(' ')
            s.long_current_price,s.short_current_price=instant_price.loc[s.long],instant_price.loc[s.short]
            s.abs_return=(s.long_current_price-s.long_price)*s.long_lot_size*s.long_lot_count - (s.short_current_price-s.short_price)*s.short_lot_size*s.short_lot_count
            s.loc['return'] = '%.2f%%'%(s.abs_return / (s.long_volume + s.short_volume ) *100)
            if abs(last_zs.loc[s.pair])<k0:
                s.close_mark= 0
            elif abs(last_zs.loc[s.pair])>k2:
                s.close_mark=-1
            else:
                s.close_mark=np.nan
            s.zscore=last_zs.loc[s.pair]
            renewal_pos=renewal_pos.append(s)
            if hist_log is not None:
                if not s.isna().close_mark:
                    #plot new closed
                    tail_pairs(s.pair,all_price.iloc[-zs_window:],zs.iloc[-zs_window:],hist_log,time_now)
                elif (type(plot_mark) in (list,tuple)) and (s.pair in plot_mark):
                    tail_pairs(s.pair,all_price.iloc[-zs_window:],zs.iloc[-zs_window:],hist_log,time_now)
                elif (type(plot_mark) is str) and (s.pair == plot_mark):
                    tail_pairs(s.pair,all_price.iloc[-zs_window:],zs.iloc[-zs_window:],hist_log,time_now)
        else:
            # already closed
            renewal_pos=renewal_pos.append(last_pos.loc[inx])
    
    renewal_pos.to_csv(log_path,float_format='%.2f',index=False,
                       columns=['pair',
                                'open_date',
                                'open_time',
                                'long',
                                'long_price',
                                'long_current_price',
                                'long_lot_size',
                                'long_lot_count',
                                'short',
                                'short_price',
                                'short_current_price',
                                'short_lot_size',
                                'short_lot_count',
                                'current_date',
                                'current_time','close_mark','abs_return','return','long_adj_price','long_volume','short_adj_price','short_volume','volume_delta','zscore'])
    
    # tail potential
    if potential_path is not None:
        po_pairs=pd.read_csv(potential_path).mark.tolist()
        if not zs_log:
            ratio,zscore=zscore_w(all_price,po_pairs,window=zs_window)
        else:
            ratio,zscore=zscore_log_w(all_price,po_pairs,window=zs_window)
        print('\npotential zs:')
        print(zscore.iloc[-1])
    return 0


    
    
def last_hk(log_path,hist_price,w,zs_window=20,k0=1,k2=4,zs_log=False):
    '''
    log_path: path to store log file. log file should contains headers: pair,open_date,open_time,long,long_price,long_current_price,long_lot_size,long_lot_count,short,short_price,short_current_price,short_lot_size,short_lot_count,current_date,current_time,close_mark,abs_return,return,long_adj_price,long_volume,short_adj_price,short_volume,volume_delta
    hist_price: historical price with specific length of trading times.
    zs_window: window to calculate zscore.
    w: from WindPy import w
    zs_log: whether to use log zscore instead of normal zscore. This should be the same as in back test.
    k0: thresh to close position
    k2: thresh to close out position
        
    return
        0,1,2,3 as in check_time_hk returns
    '''
    last_pos=pd.read_csv(log_path)
    # find pairs
    pairs=last_pos.pair.loc[last_pos.close_mark.isna()].tolist()
    tickers=list(np.unique('|'.join(pairs).split('|')))
    instant_price,adjfactor,time_now=load_instant_price(tickers,w,adj=None)
    print('\n\n\n\n',time_now)
    ft=check_time_hk(time_now)
    if ft !=3:
        return ft
    elif instant_price.shape[0]==0:
        return ft
        
    all_price=hist_price[tickers].append(instant_price.mul(adjfactor)).iloc[1:]
    if not zs_log:
        ratio,zscore=zscore_w(all_price,pairs,window=zs_window)
    else:
        ratio,zscore=zscore_log_w(all_price,pairs,window=zs_window)
    last_price,last_zs=all_price.iloc[-1],zscore.iloc[-1]    
    stabel_p=filter_pval(all_price,pairs,multi=False)
    non_station=list(set(pairs).difference(set(stabel_p)))        
    renewal_pos=pd.DataFrame()
    for inx in last_pos.index:
        if last_pos['close_mark'].isna().loc[inx]:
            # not closed yet
            s=last_pos.loc[inx]
            s.current_date,s.current_time=time_now.split(' ')
            s.long_current_price,s.short_current_price=instant_price.loc[s.long],instant_price.loc[s.short]
            s.abs_return=(s.long_current_price-s.long_price)*s.long_lot_size*s.long_lot_count - (s.short_current_price-s.short_price)*s.short_lot_size*s.short_lot_count
            s.loc['return'] = '%.2f%%'%(s.abs_return / (s.long_volume + s.short_volume ) *100)
            if s.pair in non_station:
                s.close_mark = 1
                print('Non-stationary',s.pair)
            elif abs(last_zs.loc[s.pair])<k0:
                s.close_mark = 0
                print('Returned',s.pair)
            elif abs(last_zs.loc[s.pair])>k2:
                s.close_mark = -1
                print('Closed out',s.pair)
            else:
                s.close_mark = np.nan
            s.zscore=last_zs.loc[s.pair]
            renewal_pos=renewal_pos.append(s)
        else:
            # already closed
            renewal_pos=renewal_pos.append(last_pos.loc[inx])
    renewal_pos.to_csv(log_path,float_format='%.2f',index=False,columns=last_pos.columns)        
    return 3