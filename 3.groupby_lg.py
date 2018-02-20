#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:58:31 2018

@author: cchenbe
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
from statsmodels.regression.linear_model import OLS
from sklearn.linear_model import LinearRegression

data = pd.read_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/DATA.csv')
#fillna,inf
data['ac_nochange'].interpolate(method='akima',inplace=True)
data['prcc'].interpolate(method='pchip',inplace=True)
data['BTM'].fillna(1,inplace=True)
del data['uniami']
data.replace([np.inf,-np.inf],np.nan,inplace=True)
data.dropna(axis=0,inplace=True)
nan_0001=np.array([np.inf, -np.inf, np.nan, -0.0001, 0.0001])

#list
params_list=[]
tvalues_list=[]
predict_list=[]
grouped = data.groupby(['gvkey_x'])
for name,group in grouped:
    #条件：数据量大于 1
    if len(group['gvkey_x'])>2:
        #建立array
        epspi=np.array(group['epspi'])
        NEGE=np.array(group['NEGE'])
        DD=np.array(group['DD'])
        dvpsp=np.array(group['dvpsp'])
        BTM=np.array(group['BTM'])
        prcc=np.array(group['prcc'])
        acc=group['ac_nochange'].diff(1)
        acc.replace([np.inf,-np.inf],np.nan,inplace=True)
        acc.fillna(0.0001,inplace=True)
        
        #build ag
        at_grow=group['at'].diff(1)
        middle=list(at_grow)
        middle.pop(0) #删除指定项
        middle.append(0.0001)
        at=group['at']
        ag=middle/at
        ag.replace([np.inf,-np.inf],np.nan,inplace=True)
        ag.fillna(0.000001,inplace=True)

        #build Et
        et=group['epspi']
        h=np.delete(np.array(et),0)
        Et=np.append(h,0.0001)

        #建立字典,df
        dic={'epspi':epspi,'NEGE':NEGE,'DD':DD,'dvpsp':dvpsp,'BTM':BTM,'prcc':prcc,'acc':acc,'ag':ag,'Et':Et}
        group_frame=pd.DataFrame(dic)
        #标准化X_s_nd
        Xframe=group_frame[['epspi','acc','dvpsp','prcc','ag','BTM']]
        Xmin,Xmax=Xframe.min(),Xframe.max()
        X_s = (Xframe-Xmin)/(Xmax-Xmin)
        X_s.fillna(0.0001,inplace=True)
        #建立回归方程X，y
        X=pd.concat([X_s,group_frame[['NEGE','DD']]],axis=1)
        y = group_frame['Et']
        
        data1=pd.concat([X,y],axis=1)
        result = sm.ols(formula="y~X",data=data1).fit()
        #parameters&tvalues
        parameters=np.array(result.params)
        params_list.append(parameters)
        tvalues=np.array(result.tvalues)
        tvalues_list.append(tvalues)
        '''
        #predict
        linreg = LinearRegression()
        model = linreg.fit(X,y)
        predicts=linreg.predict(X)
        dic1={'Et':Et,'Pre':predicts}
        pre_frame=pd.DataFrame(dic1)
        '''
param_cols = ['int','epspi','acc','dvpsp','prcc','ag','BTM','NEGE','DD']
Param = pd.DataFrame(params_list,columns=param_cols)  
Param.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/Param.csv',index=False)

Tvalues=pd.DataFrame(tvalues_list,columns=param_cols)
Tvalues.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/Tvalues.csv',index=False)









    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
