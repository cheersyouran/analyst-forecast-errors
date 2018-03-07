# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import wrds
db = wrds.Connection()
import pandas as pd
import numpy as np
import datetime
#gvkey, cusip, fyear, datadate
key_variables = db.raw_sql('SELECT gvkey, cusip, fyear, datadate FROM comp.funda')
key_variables.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/key_variables.csv',index = False)
#key_variables=pd.read_csv('/Users/chongchen/Desktop/PROJECT/CF_AF/key_variables.csv')
'''
data1:
Current Assets - Total,Assets - Total,Book Value Per Share,Cash and Short-Term Investments
Common/Ordinary Stock (Capital),Debt in Current Liabilities - Total,Current Liabilities - Total
Earnings Per Share (Basic) - Including Extraordinary ItemsE
'''
data1 = db.raw_sql("SELECT gvkey,datadate,IB,CSTK,ACT,DLC,CHE,LCT,AT,CEQ,CSHO,DVC\
                   FROM comp.co_afnd1 \
                   WHERE indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                   AND AT>0\
                   AND datadate between '1979-06-01' and '2010-05-31' ")
data1.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data1.csv',index = False)
#data1=pd.read_csv('/Users/chongchen/Desktop/PROJECT/CF_AF/data1.csv')
'''
data2:Dividends per Share - Pay Date,Price Close - Annual,Market Value - Total
'''
data2 = db.raw_sql("SELECT gvkey,datadate\
                   FROM compa.co_amkt\
                   WHERE curcd='USD'\
                   AND datadate between '1979-06-01' and '2010-05-31' ")
data2.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data2.csv',index = False)
#data2=pd.read_csv('/Users/chongchen/Desktop/PROJECT/CF_AF/data3.csv')
'''
data3:sale >0
'''
data3=db.raw_sql("SELECT gvkey,datadate,SPI FROM compa.co_afnd2 \
                 WHERE SALE >0 \
                 AND indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                 AND datadate between '1979-06-01' and '2010-05-31' ")
data3.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data3.csv',index = False)

#data4
data4=db.raw_sql("SELECT gvkey,datadate,prcc_f FROM compa.funda \
                 WHERE indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                 AND datadate between '1979-06-01' and '2010-05-31' ")
data4.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data4.csv',index = False)

#data5 adjust shares outstanding
#cusip,ticker,holding period return(monthly) number of shares outstanding cumulative factor to adjust shares

#merge data1 data2 data3
data1=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data1.csv')
data2=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data2.csv')
data3=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data3.csv')
data4=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data4.csv')
data5=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data5.csv')
data5['SHROUT']=data5['SHROUT']*1000  #number of shares outstanding recorded in thousands

middle=pd.merge(data1,data2,on=['gvkey','datadate'])
middle1=pd.merge(data3,data4,on=['gvkey','datadate'])
comp=pd.merge(middle,middle1,on=['gvkey','datadate'])
comp.drop_duplicates(['gvkey','datadate'],keep='last',inplace=True)

#build EARNINGS feature
comp['spi'].fillna(0,inplace=True)
comp['earnings']=comp['ib']-comp['spi']*0.65
comp['E']=comp['earnings']/comp['csho']
comp['DIV']=comp['dvc']/comp['csho']
#comp['DIV'].fillna(0,inplace=True)
comp.replace([np.inf, -np.inf], np.nan,inplace=True) 

#link data(link IBES and COMP)
data_link=db.raw_sql('SELECT gvkey,cusip,ibtic FROM comp.security')
data_link.dropna(inplace=True)
data_link.drop_duplicates(keep='last',inplace=True)
data_link.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data_link.csv',index = False)
data_link=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/data_link.csv')

#AF data 
AF=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/AF.csv')
del AF['FPI']
del AF['MEASURE']
#筛选距离fiscal year end超过7个月的AF预测数据
AF1=AF[pd.to_datetime(AF['FPEDATS']) - datetime.timedelta(days=214) >pd.to_datetime(AF['STATPERS'])]
AF1.drop_duplicates(['CUSIP','FPEDATS'],keep='last')
#添加AF的FYEAR(calender year to fiscal year) 
AF1['FYEAR']=AF1['FPEDATS'].apply(lambda x:pd.to_datetime(x).year-1 \
   if pd.to_datetime(x).month<6 else pd.to_datetime(x).year)
#merge AF and data_link (link IBES and COMP)       
AF_data=pd.merge(AF1,data_link,left_on='TICKER',right_on='ibtic')
AF_data.rename(columns={'CUSIP':'CUSIP_8','cusip':'CUSIP_9'}, inplace=True)
del AF_data['ibtic']
AF_data.drop_duplicates(['TICKER','FYEAR'],keep='last',inplace=True)
AF_data.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/AF_data.csv',index = False)
#comp_data是所有comp数据库中的数据合集
key_variables=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/key_variables.csv')
comp_data=pd.merge(comp,key_variables,on=['gvkey','datadate'])
comp_data.drop_duplicates(['gvkey','datadate','cusip','fyear'],keep='last',inplace=True)
comp_data.rename(columns={'cusip':'CUSIP_9','fyear':'fyear_t_1'}, inplace=True)
comp_data.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/comp_data.csv',index = False)
#build CF_data
del data5['TICKER']










