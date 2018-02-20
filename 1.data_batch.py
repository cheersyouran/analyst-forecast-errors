# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import wrds
db = wrds.Connection()
import pandas as pd
import numpy as np

db = wrds.Connection()
#gvkey, cusip, fyear, datadate
key_variables = db.raw_sql('SELECT gvkey, cusip, fyear, datadate FROM comp.funda')
key_variables.to_csv('/Users/cchenbe/Desktop/key_variables.csv',index = False)

"""
data1:
Current Assets - Total,Assets - Total,Book Value Per Share,Cash and Short-Term Investments
Common/Ordinary Stock (Capital),Debt in Current Liabilities - Total,Current Liabilities - Total
Earnings Per Share (Basic) - Including Extraordinary ItemsE
"""
data1 = db.raw_sql("SELECT gvkey,datadate,act,at,bkvlps,che,cstk,dlc,lct,epspi\
                   FROM comp.co_afnd1 \
                   WHERE indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                   AND datadate between '1989-12-31' and '2010-12-31' ")
data1.to_csv('/Users/cchenbe/Desktop/data1.csv',index = False)

"""
data2:Net Income before Extraordinary Items and after Noncontrolling Interest
"""
data2 = db.raw_sql("SELECT gvkey,datadate,UNIAMI FROM comp.co_afnd2 \
                   WHERE datadate between '1989-12-31' and '2010-12-31' ")
data2.to_csv('/Users/cchenbe/Desktop/data2.csv',index = False)

"""
data3:Dividends per Share - Pay Date,Price Close - Annual,Market Value - Total
"""
data3 = db.raw_sql("SELECT gvkey,datadate,DVPSP,PRCC,MKVALT\
                   FROM compa.co_amkt\
                   WHERE curcd='USD'\
                   AND datadate between '1989-12-31' and '2010-12-31' ")
data3.to_csv('/Users/cchenbe/Desktop/data3.csv',index = False)

#link data
data_link=db.raw_sql('SELECT gvkey,cusip,ibtic\
                     FROM comp.security')
data_link.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/data_link.csv',index = False)

'''AF data python拉取的数据不全，没有2000年以前的数据
AF=db.raw_sql("SELECT ticker,cusip,statpers,fpi,meanest,fpedats,numest\
              FROM ibes.secdssumu\
              WHERE fiscalp='ANN' and usfirm='1'\
              AND fpedats between '1988-12-31' and '2000-12-31' ")
'''
AF=pd.read_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF.csv')
AF.drop_duplicates(['CUSIP','FPEDATS'],keep='last',inplace=True)
AF['YEAR']=AF['FPEDATS'].apply(lambda x:pd.to_datetime(x).year)

AF.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF1.csv',index = False)
del AF['TICKER']
del AF['STATPERS']
del AF['MEASURE']
del AF['FPI']
del AF['USFIRM']
del AF['FPEDATS1']
AF.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF_simple.csv',index = False)

#ibes ticker
ibes_ticker=db.raw_sql("SELECT ticker,cusip,sdates\
                       FROM ibes.idsum\
                       WHERE usfirm='1'")
ibes_ticker.drop_duplicates(['cusip'],keep='last',inplace=True)
ibes_ticker.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/ibes_ticker.csv',index = False)

"""
To link Compustat GVKEY with IBES Ticker the application uses a two-step approach.
First, it uses a header map between GVKEY and IBES Ticker provided in Compustat Security table (IBTIC variable).
This approach yield 11,869 distinct GVKEYs with IBES Ticker match, but still leaves 17,889 GVKEYs
without matched IBES ticker (using mid 2010 vintages of IBES and Compustat). 
For those GVKEYs that have missing IBTIC in Compustat and a valid PERMNO (12,225 GVKEYs), the existing link is
supplemented with additional historical GVKEY-IBES ticker links (7,142 additional GVKEY-IBES Ticker
matches) obtained by, first, merging the rest of GVKEYS with PERMNOs on a historical basis using
CRSP-Compustat Merged Database (CCMXPF_linktable in /wrds/crsp/sasdata/cc/) and, second, by
bringing in additional IBES Tickers from the IBES-PERMNO link 

"""
crsp_permno=db.raw_sql('SELECT permno,ncusip FROM crspa.stocknames')

ibtic=db.raw_sql("SELECT gvkey,cusip,ibtic\
                 FROM comp.security\
                 WHERE excntry='USA' ")
#connect ibes and comp 
link1=pd.merge(ibtic,ibes_ticker,left_on='ibtic',right_on='ticker')
del link1['ibtic']
del link1['sdates']
link1.drop_duplicates(['ticker'],keep='last',inplace=True)
link1.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/link.csv',index = False)

link2=pd.merge(ibes_ticker,link1,left_on='cusip',right_on='cusip_y')
del link2['ticker_y']
del link2['cusip']
#connect AF and comp
AF_comp=pd.merge(AF,link2,left_on='CUSIP',right_on='cusip_y')
del AF_comp['sdates']
del AF_comp['CUSIP']
del AF_comp['FPEDATS']

AF_comp.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF_comp.csv',index = False)
data_nodu = pd.read_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/data_nodu.csv')
del data_nodu['datadate']

AF_CF=pd.merge(data_nodu,AF_comp,left_on=['cusip','fyear'],right_on=['cusip_x','YEAR'])
del AF_CF['cusip']
del AF_CF['YEAR']
AF_CF.to_csv('/Users/cchenbe/Desktop/CF_AF/raw_data/AF_CF.csv',index = False)











