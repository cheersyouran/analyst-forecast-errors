#!/usr/bin/env python3
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats 
from sklearn.cross_validation import train_test_split
from codes.config import config
from sklearn import linear_model

cf_af = pd.read_csv(config.cf_af)

def apply(x):
    x_ = x.copy()
    x_[x_ > x_.quantile(0.995)] = None
    x_[x_ < x_.quantile(0.005)] = None
    return x_

cf_af['ag'] = cf_af.groupby(['fyear_t_1'])['ag'].apply(func=apply)
cf_af['BTM'] = cf_af.groupby(['fyear_t_1'])['BTM'].apply(func=apply)
cf_af['MEANEST'] = cf_af.groupby(['fyear_t_1'])['MEANEST'].apply(func=apply)
cf_af['RE'] = cf_af.groupby(['fyear_t_1'])['RE'].apply(func=apply)
cf_af['at_ps'] = cf_af.groupby(['fyear_t_1'])['at_ps'].apply(func=apply)
cf_af['DIV'] = cf_af.groupby(['fyear_t_1'])['DIV'].apply(func=apply)
cf_af['prcc_f'] = cf_af.groupby(['fyear_t_1'])['prcc_f'].apply(func=apply)
cf_af['E_p'] = cf_af.groupby(['fyear_t_1'])['E_p'].apply(func=apply)
cf_af['ACC_P'] = cf_af.groupby(['fyear_t_1'])['ACC_P'].apply(func=apply)
cf_af['ACC_N'] = cf_af.groupby(['fyear_t_1'])['ACC_N'].apply(func=apply)

cf_af = cf_af.dropna()

def regression(data):
    X = data[['E_p', 'NEGE', 'ACC_N', 'ACC_P', 'ag', 'DD', 'BTM', 'prcc_f', 'DIV']]
    Y = data['RE']

    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=1)

    model = linear_model.LinearRegression()
    model.fit(X, Y)
    model.coef_
    return np.hstack((model.intercept_, model.coef_))


result = cf_af.groupby(['fyear_t_1']).apply(func=regression)
print(np.mean(result.values))

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