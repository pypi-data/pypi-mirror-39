# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 17:03:09 2018

@author: yili.peng
"""
from math import gcd
import numpy as np

def coprime(x,y):
    return gcd(x,y)==1

def estimate(decimal,n):
    lower=(0,1)
    upper=(1,1)
    for x in range(2,n+1):
        for y in range(int(np.floor(x*lower[0]/lower[1])+1),int(np.ceil(x*upper[0]/upper[1]))):
            if coprime(x,y):
                if y/x > decimal:
                    upper=(y,x)
                if y/x <= decimal:
                    lower=(y,x)    
    dl=decimal-lower[0]/lower[1]
    du=upper[0]/upper[1]-decimal
    return ((lower,dl) if dl<du else (upper,du))

def match(price1,price2,lotsize1,lotsize2,n=10,m=None):
    '''
    n: Max lot of the stock with larger price
    m: Max amount of the stock with larger price. Use n if set None (default) 
    '''
    p1=price1*lotsize1
    p2=price2*lotsize2
    p11,p21=((p2,p1) if p1<p2 else (p1,p2))
    #p11>p21
    n=(n if m is None else int(m//p11))
#    result=[]
    a=p11//p21
    b=p11/p21-a
    est,err=estimate(b,n)
    lot21,lot11=int(est[0]+est[1]*a),est[1] 
    lot1,lot2 = ((lot21,lot11) if p1<p2 else (lot11,lot21))
    return lot1,lot2
