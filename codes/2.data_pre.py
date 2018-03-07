# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

comp_data=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/comp_data.csv')
'''
comp_data['ib'].interpolate(method='linear',inplace=True) 
comp_data['cstk'].interpolate(method='linear',inplace=True) 
comp_data['act'].interpolate(method='linear',inplace=True) 
comp_data['dlc'].interpolate(method='linear',inplace=True) 
comp_data['che'].interpolate(method='linear',inplace=True)
comp_data['lct'].interpolate(method='linear',inplace=True)
comp_data['at'].interpolate(method='linear',inplace=True)
comp_data['csho'].interpolate(method='linear',inplace=True)
comp_data['prcc_f'].interpolate(method='linear',inplace=True)  
'''  
comp_data.replace([np.inf, -np.inf], np.nan,inplace=True)    
comp_data.dropna(inplace=True)

#NEGE negative earnings indicator 
def NEGE(number):
    if number < 0:
        return 1
    else:
        return 0
comp_data['NEGE'] = comp_data['E'].map(NEGE)

#DD non-dividend indicator 
comp_data['DIV'].fillna(0)
def DD(number):
    if number > 0:
        return 0
    else:
        return 1
comp_data['DD'] = comp_data['DIV'].map(DD)
    
#BTM = book values scaled by market value of equity
prcc_p=np.abs(comp_data['prcc_f'])
comp_data['BTM'] = comp_data['ceq']/(prcc_p*comp_data['csho'])
comp_data['accruals_nochange'] = comp_data['act']+comp_data['dlc']-comp_data['che']-comp_data['lct']
#per-share
comp_data['ac_nochange']=comp_data['accruals_nochange']/comp_data['csho']
comp_data.dropna(inplace=True)
#total asset per share
comp_data['at_ps']=comp_data['at']/comp_data['cstk']
comp_data.replace([np.inf, -np.inf], np.nan,inplace=True)    
comp_data.dropna(inplace=True)
#comp_data.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/comp_data1.csv',index=False)

#merge AF_data and comp_data(pay attention to time series)
AF_data=pd.read_csv('/Users/chongchen/Dropbox/CF_AF/data_new/AF_data.csv')
AF_data['fyear_t_1']=AF_data['FYEAR']-1
E_y=comp_data[['gvkey','fyear_t_1','E']]
E_y['fyear_t_1']=E_y['fyear_t_1']-1
E_y.rename(columns={'E':'RE'}, inplace=True)
middle=pd.merge(comp_data,AF_data,on=['gvkey','CUSIP_9','fyear_t_1'])
CF_AF=pd.merge(middle,E_y,on=['gvkey','fyear_t_1'])

#按每家公司goupby以后计算每家公司每一年的AG和ACC
gvkey1,datadate1,E1,div1,prcc_f_1,CUSIP_91,fyear_t_11,NEGE1=[],[],[],[],[],[],[],[]
DD1,BTM1,at_ps1,TICKER1,CUSIP_81,NUMEST1,MEANEST1,FYEAR1,RE1=[],[],[],[],[],[],[],[],[]
ACC1,AG1,csho1=[],[],[]
grouped=CF_AF.groupby(comp_data['gvkey'])
for name,group in grouped:
    if len(group['gvkey'])>1:
        #需要保留的features
        gvkey=group['gvkey']
        datadate=group['datadate']
        E=group['E']
        div=group['DIV']
        prcc_f=group['prcc_f']
        CUSIP_8=group['CUSIP_8']
        CUSIP_9=group['CUSIP_9']
        fyear_t_1=group['fyear_t_1']
        NEGE=group['NEGE']
        DD=group['DD']
        BTM=group['BTM']
        at_ps=group['at_ps']
        TICKER=group['TICKER']
        NUMEST=group['NUMEST']
        MEANEST=group['MEANEST']
        FYEAR=group['FYEAR']
        RE=group['RE']
        csho=group['csho']
        #build ACC
        ACC=group['ac_nochange'].diff()
        #build AG
        at=group['at']
        at_grow=at.diff(1)
        middle=list(at)
        middle.insert(0,1)
        middle.pop(-1)        #分母数列下移一位,插入1在首位,与nan相除后为nan
        AG=at_grow/middle
        #extend
        gvkey1.extend(gvkey)
        datadate1.extend(datadate)
        E1.extend(E)
        div1.extend(div)
        prcc_f_1.extend(prcc_f)
        CUSIP_81.extend(CUSIP_8)
        CUSIP_91.extend(CUSIP_9)
        fyear_t_11.extend(fyear_t_1)
        NEGE1.extend(NEGE)
        DD1.extend(DD)
        BTM1.extend(BTM)
        at_ps1.extend(at_ps)
        TICKER1.extend(TICKER)
        NUMEST1.extend(NUMEST)
        MEANEST1.extend(MEANEST)
        FYEAR1.extend(FYEAR)
        RE1.extend(RE)
        ACC1.extend(ACC)
        AG1.extend(AG)
        csho1.extend(csho)
        
dic={'gvkey':gvkey1,'datadate':datadate1,'E':E1,'div':div1,'prcc_f':prcc_f_1,\
     'CUSIP_8':CUSIP_81,'CUSIP_9':CUSIP_91,'fyear_t_1':fyear_t_11,'NEGE':NEGE1,'DD':DD1,\
     'BTM':BTM1,'at_ps':at_ps1,'TICKER':TICKER1,'NUMEST':NUMEST1,'MEANEST':MEANEST1,'FYEAR':FYEAR1,\
     'RE':RE1,'ACC':ACC1,'AG':AG1,'csho':csho1}
group_frame=pd.DataFrame(dic)
group_frame.replace([np.inf, -np.inf], np.nan,inplace=True)    
group_frame.dropna(inplace=True)
   
#ACC+ ACC-
def ACC_P(number):
    if number >= 0:
        return number
    else:
        return None
group_frame['ACC_P'] = group_frame['ACC'].map(ACC_P)

def ACC_N(number):
    if number < 0:
        return number
    else:
        return None
group_frame['ACC_N'] = group_frame['ACC'].map(ACC_N)

#E+
def E_p(number):
    if number >= 0:
        return number
    else:
        return 0
group_frame['E_p'] = group_frame['E'].map(E_p)


group_frame.replace([np.inf, -np.inf], np.nan,inplace=True)   
group_frame.fillna(0,inplace=True)

group_frame.to_csv('/Users/chongchen/Dropbox/CF_AF/data_new/group_frame.csv',index=False)


























