# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
df = pd.read_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF_CF.csv')

#NEGE
def NEGE(number):
    if number > 0:
        return 1
    else:
        return 0
df['NEGE'] = df['epspi'].map(NEGE)

#DD
df['dvpsp'].fillna(0)
def DD(number):
    if number > 0:
        return 1
    else:
        return 0
df['DD'] = df['dvpsp'].map(DD)

#BTM = book values caled by market value of equity
df['market_value_pershare'] = df['mkvalt']/df['lct']
df['BTM'] = df['bkvlps']/df['market_value_pershare']

"""
Accruals = the change in current assets+ the change in debt in current liabilities
- change in cashand short-term investments  - change in current liabilities 
"""

df['accruals_nochange'] = df['act']+df['dlc']-df['che']-df['lct']

#统一单位
df['act']=df['act']*1000000
df['at']=df['at']*1000000
df['che']=df['che']*1000000
df['cstk']=df['cstk']*1000000
df['dlc']=df['dlc']*1000000
df['lct']=df['lct']*1000000
df['uniami']=df['uniami']*1000000
df['mkvalt']=df['mkvalt']*1000000
df['accruals_nochange']=df['accruals_nochange']*1000000
print(df)

#per-share
df['ac_nochange']=df['accruals_nochange']/df['cstk']
df.drop_duplicates(['gvkey_x','fyear'],keep='last')
df.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/DATA.csv',index=False)
























