# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:07:17 2018

@author: yili.peng
"""
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

convert=lambda x : datetime.strptime(str(x),'%Y%m%d')
def change_index(df):
    new_inx=[convert(str(x)) for x in df.index]
    df_new=df.copy()
    df_new.index=new_inx
    return df_new

def tail_pairs(pair,price,zscore,time,time_span=None,log=None,**kwargs):
    '''
    plot pairs
    pair: one pair 
    '''
    time_span=(min(price.shape[0],zscore.shape[0]) if time_span is None else time_span)
    if (log is not None) and (pair in log.mark.tolist()):
        ticker1,ticker2=pair.split('|')
        p1=price[ticker1].iloc[-time_span:]
        p2=price[ticker2].iloc[-time_span:]
        sub_pos=log.loc[log.mark==pair]
        sub_pos.period=sub_pos.open_dt//10000
        
        yr=[]
        po=[]
        ne=[]
        ar=[]
        for key,gp in sub_pos.groupby('id').agg({'period':max,'abs_returns':sum}).groupby('period'):
            yr.append(str(key))
            po.append(gp.query('abs_returns>=0').shape[0])
            ne.append(gp.query('abs_returns<0').shape[0])
            ar.append(round(gp.abs_returns.mean()/10,3))
        total_wr=sum(po)/(sum(po)+sum(ne))
        mean_ar=round(sub_pos.abs_returns.mean()/10,3)
        
        plt.style.use('default')
        plt.figure(figsize=(16,6))
    #    fig, axes =plt.subplots(nrows=3,figsize=(10,7.5),dpi=100,**kwargs)
        ax00 = plt.subplot(221)
        ax01=ax00.twinx()
        l1=ax00.plot(change_index(p1),'.-',color='#1f77b4',label=p1.name)
        l2=ax01.plot(change_index(p2),'.-',color='#ff7f0e',label=p2.name)
        ax00.annotate(str(round(change_index(p1).iloc[-1],3)),(change_index(p1).index[-1],change_index(p1).iloc[-1]))
        ax01.annotate(str(round(change_index(p2).iloc[-1],3)),(change_index(p2).index[-1],change_index(p2).iloc[-1]))
        ll=l1+l2
        lab=[l.get_label() for l in ll]
        ax00.legend(ll,lab,loc=0)
        ax00.grid(linestyle=':')
        ax00.set_ylabel(p1.name)
        ax01.set_ylabel(p2.name)
        ax00.set_xticklabels([])
        ax00.set_title('\n'.join([pair,time]))
        ax10=plt.subplot(223)
        ax10.plot(change_index(zscore[pair].iloc[-time_span:]),'.-',label='zscore',color='#d62728')
        ax10.set_yticks(range(-3,4), minor=True)
        ax10.xaxis.grid(True,linestyle=':')
        ax10.yaxis.grid(True,linestyle=':',which='minor')
        ax10.legend(loc=0)
        ax20=plt.subplot(143)
        ax20.bar(yr,ne,color='#2ca02c',alpha=0.3,width=0.1)
        ax20.bar(yr,po,bottom=ne,color='#d62728',alpha=0.5,width=0.1)
        ax20.yaxis.grid(linestyle=':')
        ax20.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax20.set_ylabel('number')
        ax21=ax20.twinx()
        ax21.plot(yr,ar,marker='.',linestyle='--',alpha=1,color='#bcbd22')
        for i, txt in enumerate(ar):
            ax21.annotate(str(round(txt,3)), (yr[i], ar[i]))
        ax21.set_ylabel('returns')
        ax21.set_title('\n'.join(['win rate: %.3f'%total_wr,'mean return: %.3f'%mean_ar]))
        plt.gcf().autofmt_xdate()
        plt.show()
    else:
        ticker1,ticker2=pair.split('|')
        p1=price[ticker1].iloc[-time_span:]
        p2=price[ticker2].iloc[-time_span:]
        plt.style.use('default')
        plt.figure(figsize=(16,6))
    #    fig, axes =plt.subplots(nrows=3,figsize=(10,7.5),dpi=100,**kwargs)
        ax00 = plt.subplot(221)
        ax01=ax00.twinx()
        l1=ax00.plot(change_index(p1),'.-',color='#1f77b4',label=p1.name)
        l2=ax01.plot(change_index(p2),'.-',color='#ff7f0e',label=p2.name)
        ax00.annotate(str(round(change_index(p1).iloc[-1],3)),(change_index(p1).index[-1],change_index(p1).iloc[-1]))
        ax01.annotate(str(round(change_index(p2).iloc[-1],3)),(change_index(p2).index[-1],change_index(p2).iloc[-1]))
        ll=l1+l2
        lab=[l.get_label() for l in ll]
        ax00.legend(ll,lab,loc=0)
        ax00.grid(linestyle=':')
        ax00.set_ylabel(p1.name)
        ax01.set_ylabel(p2.name)
        ax00.set_xticklabels([])
        ax00.set_title('\n'.join([pair,time]))
        ax10=plt.subplot(223)
        ax10.plot(change_index(zscore[pair].iloc[-time_span:]),'.-',label='zscore',color='#d62728')
        ax10.set_yticks(range(-3,4), minor=True)
        ax10.xaxis.grid(True,linestyle=':')
        ax10.yaxis.grid(True,linestyle=':',which='minor')
        ax10.legend(loc=0)
        plt.gcf().autofmt_xdate()
        plt.show()