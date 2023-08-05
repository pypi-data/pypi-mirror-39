# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:07:15 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mini_exchange import Mini_Exchange,Account,Log
from datetime import datetime
from .zscore import zscore_df,zscore_w,zscore_log_w,zscore_log_df
import matplotlib.dates as mdates

convert=lambda x : datetime.strptime(str(x),'%Y%m%d')
def change_index(df):
    new_inx=[convert(str(x)) for x in df.index]
    df_new=df.copy()
    df_new.index=new_inx
    return df_new

class Trade:
    def __init__(self,price,start=None,end=None):
        start=(price.index[0] if start is None else start)
        end=(price.index[-1] if end is None else end)
        self.price=price.loc[start:end]
        self.MM=Mini_Exchange(price.loc[start:end])
        self.users={}
        self.close_line=[]
        self.close_plot=[]
    def add_user(self,user_name,signal,start_amount=1000):
        '''
        signal: Dataframe as  
                -- (period,dt) * tickers:
                with Value            
                    0 or nan or other number: hold still
                    1: long
                    2: close long position
                    3: close long and open short
                    -1: short
                    -2: close short position
                    -3: close short and open long
        '''
        acc=Account(start_amount=start_amount)
        log=Log()
        self.MM.register(user_name,account=acc,log=log)
        if not isinstance(signal.index,pd.core.index.MultiIndex):
            signal=pd.concat([signal],keys=[0]) 
        self.users.update({user_name:[signal,acc,log]})
    
    def add_close_signal(self,s,close_status=2,marker='o'):
        self.close_line.append(
        """if (sub_sig==%d):
            self.MM.close(dt=dt,value=ticker_pair,by='mark',close_status=%d,user=user_name)"""%(s,close_status))
        self.close_plot.append(
        "ax0.plot(change_index(sub_pr[sub_s==%d]),'%s',ms=6,color='#777777')"%(s,marker))
            
    def trade_one(self,user_name,user_amt_srs,dt):
        '''
        trade oneday
        '''
        if dt not in self.users[user_name][0].index.levels[1][self.users[user_name][0].index.labels[1]]:
            return
        
        sub_signal=self.users[user_name][0].xs(dt,axis=0,level=1).iloc[0].fillna(0)
        period=sub_signal.name
        
        for ticker_pair,sub_sig in sub_signal[sub_signal!=0].items():
            t0,t1=ticker_pair.split('|')
            
            for l in self.close_line:
                exec(l)
            
            if (sub_sig==2):
                self.MM.close(dt=dt,value=ticker_pair,by='mark',close_status=0,user=user_name)
            elif (sub_sig==-2):
                self.MM.close(dt=dt,value=ticker_pair,by='mark',close_status=0,user=user_name)
            elif (sub_sig==1):
                
                amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                
                self.MM.long(t0,amount,dt,user=user_name,period=period,mark=ticker_pair)
                self.MM.short(t1,amount,dt,user=user_name,period=period,mark=ticker_pair,position_type='dual')
                
            elif (sub_sig==-1) :
                
                amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                
                self.MM.short(t0,amount,dt,user=user_name,period=period,mark=ticker_pair)
                self.MM.long(t1,amount,dt,user=user_name,period=period,mark=ticker_pair,position_type='dual')
            
            elif (sub_sig==3):
                
                self.MM.close(dt=dt,value=ticker_pair,by='mark',close_status=0,user=user_name)
                
                amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)                
                
                self.MM.short(t0,amount,dt,user=user_name,period=period,mark=ticker_pair)
                self.MM.long(t1,amount,dt,user=user_name,period=period,mark=ticker_pair,position_type='dual')
                
            elif (sub_sig==-3):
                self.MM.close(dt=dt,value=ticker_pair,by='mark',close_status=0,user=user_name)
                amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                self.MM.long(t0,amount,dt,user=user_name,period=period,mark=ticker_pair)
                self.MM.short(t1,amount,dt,user=user_name,period=period,mark=ticker_pair,position_type='dual')
            else:
                continue
    def trade(self,user_amt_df,start=None,end=None):
        '''
        user_amt_df: user_name,amt_type,value
        amt_type: 1 relative value
                  0 absolute value
        '''
        for s in ('user_name','amt_type','value'):
            if s not in user_amt_df.columns:
                raise Exception('wrong type of user_amt_df')
        start=(self.price.index.min() if start is None else start)
        end=(self.price.index.max() if end is None else end)
        for dt in self.price.loc[start:end].index:
            print('\rrun %d'%dt,end='\r')
            self.MM.hold(dt)
            for inx in user_amt_df.index:
                user=user_amt_df.loc[inx,'user_name']
                if user not in self.users:
                    continue
                else:
                    self.trade_one(user_name=user,user_amt_srs=user_amt_df.loc[inx],dt=dt)
            self.MM.settle(dt)

        print('')

    def get_user(self,user_name):
        return self.users[user_name][1],self.users[user_name][2]
    
    def summary(self,start=None,end=None):
        D={}
#        pp=[]
        kk=[]
        for key,lst in self.users.items():
            signal,acc,pos=lst
            D.update({key:[acc.annual_return(start,end),acc.sharpe_ratio(start,end),acc.romad(start,end),pos.win_rate(start,end,True),pos.total_trade(start,end,True),acc.draw_down(start,end)]})
#            pp.append(pos.log.groupby('period').agg({'abs_returns':sum,'id':len}).rename({'abs_returns':'value','id':'trade'},axis=1))
            kk.append(key)
        R=pd.DataFrame(D,index=['annual_return','sharpe_ratio','romad','win_rate','total_trade','mad']).T
#        P=pd.concat(pp,keys=kk,axis=1)
        with pd.option_context('display.max.columns',None):
            print('\nTotal Performance:\n')
            print(R.round(3).sort_values('annual_return',ascending=False))
#            print('\nPeriod Performance:\n')
#            print(P.round(3))

    def summary_pairs(self,user_name,period):
        signal,acc,pos=self.users[user_name]
        sp=pos.log\
                .infer_objects()\
                .query("period==%s"%str(period))\
                .groupby('mark')\
                .agg({'abs_returns':sum,'duration':np.mean,'id':len})\
                .rename({'abs_returns':'total_abs_returns','duration':'average_duration','id':'total_trade'},axis=1)\
                .round(2)\
                .sort_values('total_abs_returns',ascending=False)
        return sp
    
    def plot_trade_pair(self,user_name,pair,k0,k1,k2,window=20,use_log=False,halflife=None,start=None,end=None):
        '''
        need the right k coresponding to user_name, period and pair
        '''
        tickers=pair.split('|')
        signal,acc,pos=self.users[user_name]

        p=self.price[tickers].dropna()
        if use_log:
            if halflife is not None:
                sub_r,sub_z=(i[pair] for i in zscore_log_df(p,[pair],halflife=halflife))
            else:
                sub_r,sub_z=(i[pair] for i in zscore_log_w(price_df=p,pair_lst=[pair],window=window))
        else:
            if halflife is not None:
                sub_r,sub_z=(i[pair] for i in zscore_df(p,[pair],halflife=halflife))
            else:
                sub_r,sub_z=(i[pair] for i in zscore_w(price_df=p,pair_lst=[pair],window=window))
        sub_z.dropna(inplace=True)
        
        start=(sub_z.index.min() if start is None else start)
        end=(sub_z.index.max() if end is None else end)
        
        sub_z=sub_z.loc[start:end]
        
        sub_pr=p.reindex(sub_z.index).div(p.reindex(sub_z.index).iloc[0])
        sub_s=signal[pair].xs(0).reindex(sub_z.index)
            
        l=pos.log.query('period==%s'%str(0)).query('mark=="%s"'%pair).groupby('id').agg({'abs_returns':sum,'open_dt':np.unique,'close_dt':np.unique}).query('open_dt>=%d'%sub_s.index.min())
        x_range=[(i,j-i) for i,j in zip(mdates.date2num(l.open_dt.map(convert).tolist()),mdates.date2num(l.close_dt.map(convert).tolist()))]
        y_range=[(0,j) for j in l.abs_returns]
        c=np.where(l.abs_returns>0,'#FBC15E','#8EBA42')
        #plot
        plt.style.use('ggplot')
        fig, axes =plt.subplots(nrows=2,figsize=(16,8),dpi=100)
        ax0 = axes[0]
        ax2=ax0.twinx()
        ax0.patch.set_visible(False)
        ax2.patch.set_visible(True)
        ax0.set_zorder(ax2.get_zorder()+1)
        lines=ax0.plot(change_index(sub_pr.where(~sub_s.isna())))
        ax0.plot(change_index(sub_pr.where(sub_s.isna())),':',color='#777777')
        ax0.plot(change_index(sub_pr.loc[sub_s.isin((-1,3))]).iloc[:,0],'v',ms=6,color='#777777')
        ax0.plot(change_index(sub_pr.loc[sub_s.isin((-1,3))]).iloc[:,1],'^',ms=6,color='#777777')
        ax0.plot(change_index(sub_pr.loc[sub_s.isin((1,-3))]).iloc[:,0],'^',ms=6,color='#777777')
        ax0.plot(change_index(sub_pr.loc[sub_s.isin((1,-3))]).iloc[:,1],'v',ms=6,color='#777777')
        ax0.plot(change_index(sub_pr[sub_s.isin((2,-2))]),'o',ms=6,color='#777777')
        for l in self.close_plot:
            exec(l)
        ax0.legend(lines,list(sub_pr.columns))
        for x_var,y_var,col in zip(x_range,y_range,c):
            ax2.broken_barh((x_var,),y_var,color=col,alpha=0.5)
        ax1 = axes[1]
        ax1.plot(change_index(sub_z),label='zscore',color='#E24A33')
        ax1.axhline(y=k0, linestyle=':',color='#777777',label='k0')
        ax1.axhline(y=-k0, linestyle=':',color='#777777')
        ax1.axhline(y=k1, linestyle='-.',color='#8EBA42',label='k1')
        ax1.axhline(y=-k1, linestyle='-.',color='#8EBA42')
        ax1.axhline(y=k2, linestyle='--',color='#FBC15E')
        ax1.axhline(y=-k2, linestyle='--',color='#FBC15E',label='k2')
        ax1.legend()
        plt.gcf().autofmt_xdate()
        plt.show()
        