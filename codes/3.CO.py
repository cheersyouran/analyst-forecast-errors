#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:44:41 2018

@author: cchenbe
"""

import pandas as pd
import numpy as np
import statistics

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

co = pd.read_csv(config.correlation)

co['market_value'] = np.multiply(np.abs(co['prcc_f']),co['csho'])
co['SIZE']=np.log(1000*co['market_value'])
#co['LBM']=np.log(np.abs(co['BTM']))
co['difference']=co['RE']-co['AF']
co['BIAS']=co['difference']/co['at_ps']
co.mean()
co.replace([np.inf, -np.inf], np.nan,inplace=True)
co.dropna(inplace=True)
CO=co.sort_values(["CO"],ascending=True)
CO.reset_index(inplace=True)
CO1=CO.loc[0:10290]
CO2=CO.loc[10291:20581]
CO3=CO.loc[20582:30871]
CO4=CO.loc[30872:41162]
CO5=CO.loc[41163:51453]

CO1.mean()
CO2.mean()
CO3.mean()
CO4.mean()
CO5.mean()
np.std(CO1['AF'])
np.std(CO2['AF'])
np.std(CO3['AF'])
np.std(CO4['AF'])
np.std(CO5['AF'])
np.std(CO1['CO'])
np.std(CO2['CO'])
np.std(CO3['CO'])
np.std(CO4['CO'])
np.std(CO5['CO'])



CO1.to_csv('/Users/chongchen/Dropbox/analyst-forecast-errors/CO1.csv')
CO2.to_csv('/Users/chongchen/Dropbox/analyst-forecast-errors/CO2.csv')
CO3.to_csv('/Users/chongchen/Dropbox/analyst-forecast-errors/CO3.csv')
CO4.to_csv('/Users/chongchen/Dropbox/analyst-forecast-errors/CO4.csv')
CO5.to_csv('/Users/chongchen/Dropbox/analyst-forecast-errors/CO5.csv')

statistics.median(CO1['BIAS'])
statistics.median(CO2['BIAS'])
statistics.median(CO3['BIAS'])
statistics.median(CO4['BIAS'])
statistics.median(CO5['BIAS'])
CO1['BIAS'].mean()
CO2['BIAS'].mean()
CO3['BIAS'].mean()
CO4['BIAS'].mean()
CO5['BIAS'].mean()

data5=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data5.csv')
returns=pd.merge(CO,data5,)

AF=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/AF.csv')
CO1_date=pd.merge(CO1,AF,on=['FYEAR',])
CO1_date.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO1_date.csv')













