# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:01:17 2019

@author: xjq
"""
import pandas as pd
import numpy as np

def H_calc(date,days,stock_data): 
#date： from when to calculate H
#days: use how many days to calculate H
    #date = pd.to_datetime(date)
    stock_data = stock_data.dropna()
    if len(stock_data) > days:
        stock_data = stock_data[-days:]
    if len(stock_data)<50:
        return 0
    log_return = np.log(stock_data/stock_data.shift(1)).dropna()
    x = (log_return-np.mean(log_return))/np.std(log_return)    #Fractional Gaussian Noise
    n = np.arange(2,days)
    RS  = []
    for i in n:
        tempx = x[:i]
        Y = tempx - np.mean(tempx)
        Z = Y.cumsum()
        R = Z.max()-Z.min()
        S = tempx.std()[0]
        if S != 0:
            RS.append(R/S)
        else:
            RS.append(1)
    H = np.polyfit(np.log(n),np.log(RS),1)[0][0]
    #para = [H,log_return.mean()]   
    return H

