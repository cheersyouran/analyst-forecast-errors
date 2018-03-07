#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:13:23 2018

@author: chongchen
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats 
from sklearn.cross_validation import train_test_split
import datetime

data = pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/group_frame.csv')
#deal with outlier
params=[]
tvalues=[]
r_squares=[]
AFs=[]
predicts=[]
NUMESTs=[]
REs=[]
at_pss=[]
gvkeys=[]
CUSIP_8s=[]
FYEARs=[]
fyear_t_1s=[]
datadates=[]
cshos=[]
#groupby loop by fyear
grouped = data.groupby(['fyear_t_1'])
for name,group in grouped:
    def find_outliers1(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['AG'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'AG'] = group.loc[:,'AG'].map(find_outliers1)

    def find_outliers2(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['BTM'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'BTM'] = group.loc[:,'BTM'].map(find_outliers2)

    def find_outliers3(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['MEANEST'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'MEANEST'] = group.loc[:,'MEANEST'].map(find_outliers3)

    def find_outliers4(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['RE'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'RE'] = group.loc[:,'RE'].map(find_outliers4)

    def find_outliers5(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['at_ps'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'at_ps'] = group.loc[:,'at_ps'].map(find_outliers5)

    def find_outliers6(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['div'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'div'] = group.loc[:,'div'].map(find_outliers6)
    
    def find_outliers6(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['prcc_f'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'prcc_f'] = group.loc[:,'prcc_f'].map(find_outliers6)
    
    def find_outliers7(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['E_p'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'E_p'] = group.loc[:,'E_p'].map(find_outliers6)

    def find_outliers8(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['ACC_P'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'ACC_P'] = group.loc[:,'ACC_P'].map(find_outliers8)

    def find_outliers9(number,iq_range=0.8):
        pcnt=(1 - iq_range)/2
        qlow, median, qhigh = group['ACC_N'].quantile([pcnt, 0.50, 1-pcnt])
        iqr = qhigh - qlow
        if abs(number - median)>iqr:
            return None
        else:
            return number
    group.loc[:,'ACC_N'] = group.loc[:,'ACC_N'].map(find_outliers9)
    #fill outliers
    group.replace([np.inf, -np.inf], np.nan,inplace=True)    
    group.interpolate(method='linear',inplace=True)
    group.dropna(inplace=True)
    #linear regression model
    X=group.loc[:,['E_p','NEGE','ACC_N','ACC_P','AG','DD','BTM','prcc_f','div']]
    X=sm.add_constant(X) #给模型增加常数项
    y=group.loc[:,'RE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1) #75% 25%
    model=sm.OLS(y_test,X_test)
    results=model.fit()
    param=np.array(results.params)
    tvalue=np.array(results.tvalues)
    params.append(param)
    tvalues.append(tvalue)
    #R-squares
    r_square=results.rsquared
    r_squares.append(r_square)
    #CO frame
    gvkey=np.array(group['gvkey'])
    CUSIP_8=np.array(group['CUSIP_8'])
    datadate=np.array(group['datadate'])
    FYEAR=np.array(group['FYEAR'])
    fyear_t_1=np.array(group['fyear_t_1'])
    AF=np.array(group['MEANEST'])
    predict=np.array(results.predict(X))
    NUMEST=np.array(group['NUMEST'])
    RE=np.array(group['RE'])
    at_ps=np.array(group['at_ps'])
    csho=np.array(group['csho'])
    AFs.extend(AF)
    predicts.extend(predict)
    datadates.extend(datadate)
    NUMESTs.extend(NUMEST)
    REs.extend(RE)
    at_pss.extend(at_ps)
    gvkeys.extend(gvkey)
    CUSIP_8s.extend(CUSIP_8)
    FYEARs.extend(FYEAR)
    fyear_t_1s.extend(fyear_t_1)
    cshos.extend(csho)

#parameters
param_cols = ['Int','E_p','NEGE','acc_n','acc_p','ag','DD','BTM','prcc','div']
Param = pd.DataFrame(params,columns=param_cols)
Param.mean()
#t-values
tvalue_cols=['Int','E_p','NEGE','acc_n','acc_p','ag','DD','BTM','prcc','div']
Tvalue=pd.DataFrame(tvalues,columns=tvalue_cols)
Tvalue.mean()
#r-square
np.mean(r_squares)

#correlations
dic={'RE':REs,'AF':AFs,'CF':predicts}
correlation=pd.DataFrame(dic)
correlation.corr()
#mean error
CF_RE_error=correlation['RE']-correlation['CF']
AF_RE_error=correlation['RE']-correlation['AF']
np.mean(CF_RE_error)
np.mean(AF_RE_error)
stats.ttest_ind(correlation['RE'],correlation['CF'])
stats.ttest_ind(correlation['RE'],correlation['AF'])
#CO frame
dic1={'gvkey':gvkeys,'FYEAR':FYEARs,'fyear_t_1':fyear_t_1s,'AF':AFs,'CF':predicts,'NUMEST':NUMESTs,'RE':REs,'at_ps':at_pss}
co_frame=pd.DataFrame(dic1)
co_frame.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/co_frame.csv',index=False)
#regression of RE 
X1=co_frame.loc[:,'AF']
X2=co_frame.loc[:,'CF']
X3=co_frame.loc[:,['AF','CF']]
y=co_frame.loc[:,'RE']
X1=sm.add_constant(X1) 
X2=sm.add_constant(X2) 
X3=sm.add_constant(X3) 

model1=sm.OLS(y,X1)
result1=model1.fit()
params1=result1.params
tvalues1=result1.tvalues
result1.rsquared

model2=sm.OLS(y,X2)
result2=model2.fit()
params2=result2.params
tvalues2=result2.tvalues
result2.rsquared

model3=sm.OLS(y,X3)
result3=model3.fit()
params3=result3.params
tvalues3=result3.tvalues
result3.rsquared







      







