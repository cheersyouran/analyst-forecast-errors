#!/usr/bin/env python3
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats 
from sklearn.cross_validation import train_test_split

#设置全局路径
class Config:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.root_path = '/Users/chongchen/Dropbox/analyst-forecast-errors'
        self.data1 = self.root_path + '/data/data1.csv'
        self.data2 = self.root_path + '/data/data2.csv'
        self.data3 = self.root_path + '/data/data3.csv'
        self.data4 = self.root_path + '/data/data4.csv'
        self.data5 = self.root_path + '/data/data5.csv'
        self.link_data = self.root_path + '/data/data_link.csv'

        self.af = self.root_path + '/data/AF.csv'
        self.af_new = self.root_path + '/data/AF_new.csv'
        self.key_variables = self.root_path + '/data/key_variables.csv'
        self.comp_data = self.root_path + '/data/comp_data.csv'
        self.cf_af = self.root_path + '/data/cf_af.csv'
        self.whole_data = self.root_path + '/data/whole_data.csv'
        self.correlation = self.root_path + '/data/correlation.csv'
        

config = Config()

whole_data = pd.read_csv(config.whole_data)

def apply(x):
    x_ = x.copy()
    x_[x_ > x_.quantile(0.995)] = None
    x_[x_ < x_.quantile(0.005)] = None
    return x_

whole_data['ag'] = whole_data.groupby(['fyear_t_1'])['ag'].apply(func=apply)
whole_data['BTM'] = whole_data.groupby(['fyear_t_1'])['BTM'].apply(func=apply)
whole_data['MEANEST'] = whole_data.groupby(['fyear_t_1'])['MEANEST'].apply(func=apply)
whole_data['RE'] = whole_data.groupby(['fyear_t_1'])['RE'].apply(func=apply)
whole_data['at_ps'] = whole_data.groupby(['fyear_t_1'])['at_ps'].apply(func=apply)
whole_data['DIV'] = whole_data.groupby(['fyear_t_1'])['DIV'].apply(func=apply)
whole_data['prcc_f'] = whole_data.groupby(['fyear_t_1'])['prcc_f'].apply(func=apply)
whole_data['E_p'] = whole_data.groupby(['fyear_t_1'])['E_p'].apply(func=apply)
whole_data['ACC_P'] = whole_data.groupby(['fyear_t_1'])['ACC_P'].apply(func=apply)
whole_data['ACC_N'] = whole_data.groupby(['fyear_t_1'])['ACC_N'].apply(func=apply)
whole_data['share_aj'] = whole_data.groupby(['fyear_t_1'])['share_aj'].apply(func=apply)

DATA = whole_data[['gvkey','fyear_t_1','E_p', 'NEGE', 'ACC_N', 'ACC_P', 'ag', 'DD', 'BTM', 'prcc_f', 'DIV','RE','share_aj','MEANEST','NUMEST','at_ps','csho']]
DATA['E_p'] = DATA['E_p'].interpolate(method = 'linear')
DATA['ACC_N']= DATA['ACC_N'].interpolate(method = 'linear')
DATA['ACC_P'] = DATA['ACC_P'].interpolate(method = 'linear')
DATA['ag'] = DATA['ag'].interpolate(method = 'linear')
DATA['BTM'] = DATA['BTM'].interpolate(method = 'linear')
DATA['prcc_f'] = DATA['prcc_f'].interpolate(method = 'linear')
DATA['DIV'] = DATA['DIV'].interpolate(method = 'linear')
DATA['RE'] = DATA['RE'].interpolate(method = 'linear')
DATA['share_aj'] = DATA['share_aj'].interpolate(method = 'linear')
DATA['MEANEST'] = DATA['MEANEST'].interpolate(method = 'linear')
DATA['at_ps'] = DATA['at_ps'].interpolate(method = 'linear')

CFs = []
REs = []
AFs = []
predicts = []
prcc_fs = []
BTMs = []
at_pss = []
cshos = []
numests = []
grouped = DATA.groupby(['fyear_t_1'])
for name,group in grouped:
    X = group[['E_p', 'NEGE', 'ACC_N', 'ACC_P', 'ag', 'DD', 'BTM', 'prcc_f', 'DIV']]
    Y = group['RE']
    X = sm.add_constant(X) #给模型增加常数项
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=1)
    model = sm.OLS(y_test,X_test)
    result = model.fit()
    predict = result.predict(X)
    predicts.extend(predict)
    #CF = np.multiply(predict, group['share_aj'])
    #CFs.extend(CF)
    RE = group['RE']
    AF = group['MEANEST']
    prcc_f = group['prcc_f']
    BTM = group['BTM']
    at_ps = group['at_ps']
    csho = group['csho']
    numest = group['NUMEST']
    REs.extend(RE)
    AFs.extend(AF)
    prcc_fs.extend(prcc_f)
    BTMs.extend(BTM)
    at_pss.extend(at_ps)
    cshos.extend(csho)
    numests.extend(numest)
dic = {'RE':REs,'CF':predicts,'AF':AFs,'prcc_f':prcc_fs,'BTM':BTMs,'at_ps':at_pss,'csho':cshos,'NUMEST':numests}
correlation = pd.DataFrame(dic)
correlation.corr()

#mean error
CF_RE_error = correlation['RE']- correlation['CF']
AF_RE_error = correlation['RE']- correlation['AF']
np.mean(CF_RE_error)
np.mean(AF_RE_error)
stats.ttest_ind(correlation['RE'],correlation['CF'])
stats.ttest_ind(correlation['RE'],correlation['AF'])

#build CO
correlation['CO'] = (correlation['CF'] - correlation['AF'])/correlation['at_ps']
correlation.to_csv(config.correlation,index = False)
#regression of RE
X1=correlation.loc[:,'AF']
X2=correlation.loc[:,'CF']
X3=correlation.loc[:,['AF','CF']]
y=correlation.loc[:,'RE']
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