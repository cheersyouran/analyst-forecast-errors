#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 13:25:52 2018

@author:chongchen
"""
"""
所有股票数据形成格式统一的表格，放到同一个文件夹，运行程序后得到
系数DataFrame和Tvalues的DataFrame，在两个DF中进行全市场均值计算
"""

import pandas as pd
import numpy as np
import os
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import scipy.stats as stats
from scipy.stats import ttest_ind
#os.chdir(path)改变当前工作目录到指定的路径
os.chdir('/Users/chongchen/Desktop/PROJECT/batch_pull_in_test/')
#os.getcwd()查看修改后的工作目录
file_chdir = os.getcwd()
results_list = []#空列表
tvalues_list = []
cf_forecast_errors = []
af_forecast_errors = []
cf_af_corr = []
mean_error = []
re_t = []
#os.walk()通过在目录树中游走输出在目录中的文件名，向上或向下，即在当前工作目录中
for root,dirs,files in os.walk(file_chdir):
    for file in files: #查看每一个文件file
        if os.path.splitext(file)[1] == '.csv':
            stock = pd.read_csv(file_chdir+"/"+file)
            data = pd.DataFrame(stock)
            print(data)
            #for X,Y in data:
            feature_cols = ['EPS','NEGE','Accruals','DD','DIV','BTM','PRICE']
            X = np.array(data[feature_cols])
            y = np.array(data['EPS_N'])
            scaler = StandardScaler()
            X_s = scaler.fit_transform(X) #y没有进行归一化处理
            X_s_train,X_s_test,y_train,y_test = train_test_split(X_s,y,random_state=1)
            linreg = LinearRegression()
            model = linreg.fit(X_s_train, y_train)
            print(feature_cols,linreg.coef_)
            result = [file[:6]]
            result.extend(list(linreg.coef_))
            results_list.append(result)
            #T-test(double_sides)
            X2 = sm.add_constant(X_s)
            est = sm.OLS(y,X2)
            est2 = est.fit()
            est2.tvalues
            tvalues_list.append(est2.tvalues)
            print(tvalues_list)
            #CF prediction and prediction error,corr
            y_pred = linreg.predict(X_s) #y_pred = cf forecast
            stats.pearsonr(y,y_pred) #the second value is the P-value
            cf_forecast_errors.append(stats.pearsonr(y,y_pred))
            #AF prediction and prediction error,corr
            AF = np.array(data['AF'])
            stats.pearsonr(y,AF) #the second value is the P-value
            af_forecast_errors.append(stats.pearsonr(y,AF))
            #AF and CF corr
            stats.pearsonr(y_pred,AF)
            cf_af_corr.append(stats.pearsonr(y_pred,AF))
            #mean error
            cf_error = list(data['EPS_N'] - y_pred)
            af_error = list(data['EPS_N'] - data['AF'])
            error = cf_error.extend(af_error)
            mean_error.append(error)
            #t-statistics #Panel B最后一列的t检验，CF&RE，AF&RE
            cf_re_tstatistic,cf_re_pvalue = ttest_ind(y_pred,data['EPS_N'])
            af_re_tstatistic,af_re_pvalue = ttest_ind(y_pred,data['AF'])
            re_t_statistics = (cf_re_tstatistic,af_re_tstatistic)
            re_t.append(re_t_statistics)
            
coef_cols = ['SECUCODE','EPS','NEGE','Accruals','DD','DIV','BTM','PRICE']
Coef = pd.DataFrame(results_list,columns=coef_cols)  
tvalues_cols = ['const','EPS','NEGE','Accruals','DD','DIV','BTM','PRICE']
Tvalues = pd.DataFrame(tvalues_list,columns=tvalues_cols)
cf_forecast_errors_cols = ['t-statistics','p-values']
Cf_forecast_errors = pd.DataFrame(cf_forecast_errors,columns = cf_forecast_errors_cols)
af_forecast_errors_cols = ['t-statistics','p-values']
Af_forecast_errors = pd.DataFrame(af_forecast_errors,columns = af_forecast_errors_cols)
cf_af_corr_cols = ['t-statistics','p-values']
Cf_Af_corr = pd.DataFrame(cf_af_corr,columns = cf_af_corr_cols)
mean_error_cols = ['CF-error','AF-error']
Mean_error = pd.DataFrame(mean_error,columns = mean_error_cols)
re_cols = ['CF&RE_t','AF&RE_t']
re_t = pd.DataFrame(re_t,columns = re_cols)

print(Coef)
print(Tvalues) 
print(Cf_forecast_errors)
print(Af_forecast_errors)
print(Cf_Af_corr)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    