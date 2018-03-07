#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:44:41 2018

@author: cchenbe
"""

import pandas as pd
import numpy as np
import statistics

co_frame=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/co_frame.csv')
co_frame['CO']=(co_frame['CF']-co_frame['AF'])/co_frame['at_ps']
comp_data1=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/comp_data1.csv')
co=pd.merge(co_frame,comp_data1,on=['gvkey','fyear_t_1'])
del co['che']
del co['cstk']
del co['dlc']
del co['lct']
del co['CUSIP_9']
del co['NEGE']
del co['DD']
del co['accruals_nochange']
del co['ac_nochange']
del co['at_ps_y']

prcc_p=np.abs(co['prcc_f'])
co['market_value']=prcc_p*co['csho']
co['SIZE']=np.log(co['market_value'])
co['LBM']=np.log(abs(co['BTM']))
co['difference']=co['RE']-co['AF']
co['BIAS']=co['difference']/co['at_ps_x']
co.replace([np.inf, -np.inf], np.nan,inplace=True)
co.dropna(inplace=True)
CO=co.sort_values(["CO"],ascending=True)
CO.reset_index(inplace=True)
CO1=CO.loc[0:11057]
CO2=CO.loc[11058:22113]
CO3=CO.loc[22114:33170]
CO4=CO.loc[33171:44226]
CO5=CO.loc[44227:55282]

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



CO1.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO1.csv')
CO2.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO2.csv')
CO3.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO3.csv')
CO4.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO4.csv')
CO5.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/CO5.csv')

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













