import wrds
import pandas as pd
import numpy as np
import datetime

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
        self.key_vairables = self.root_path + '/data/key_vairables.csv'

config = Config()

def method():
   db = wrds.Connection()
   #gvkey, cusip, fyear, datadate
   data_link = db.raw_sql('SELECT gvkey,cusip,ibtic FROM comp.security')
   data_link.dropna(inplace=True)
   data_link.drop_duplicates(keep='last', inplace=True)
   data_link.to_csv(config.link_data, index=False)

   key_variables = db.raw_sql('SELECT gvkey, cusip, fyear, datadate FROM comp.funda')
   key_variables.to_csv(config.key_vairables,index = False)
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
   data1.to_csv(config.data1,index = False)
   #data1=pd.read_csv('/Users/chongchen/Desktop/PROJECT/CF_AF/data1.csv')
   '''
   data2:Dividends per Share - Pay Date,Price Close - Annual,Market Value - Total
   '''
   data2 = db.raw_sql("SELECT gvkey,datadate\
                      FROM compa.co_amkt\
                      WHERE curcd='USD'\
                      AND datadate between '1979-06-01' and '2010-05-31' ")
   data2.to_csv(config.data2,index = False)
   #data2=pd.read_csv('/Users/chongchen/Desktop/PROJECT/CF_AF/data3.csv')
   '''
   data3:sale >0
   '''
   data3=db.raw_sql("SELECT gvkey,datadate,SPI FROM compa.co_afnd2 \
                    WHERE SALE >0 \
                    AND indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                    AND datadate between '1979-06-01' and '2010-05-31' ")
   data3.to_csv(config.data3,index = False)

   #data4
   data4=db.raw_sql("SELECT gvkey,datadate,prcc_f FROM compa.funda \
                    WHERE indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'\
                    AND datadate between '1979-06-01' and '2010-05-31' ")
   data4.to_csv(config.data4,index = False)

   #data5 adjust shares outstanding
   #cusip,ticker,holding period return(monthly) number of shares outstanding cumulative factor to adjust shares

   #merge data1 data2 data3

def gen_AF():
   #link data(link IBES and COMP)
   data_link = pd.read_csv(config.link_data)
   AF = pd.read_csv(config.af, parse_dates=['FPEDATS'])

   #筛选距离fiscal year end超过7个月的AF预测数据
   AF_new = AF[pd.to_datetime(AF['FPEDATS']) - datetime.timedelta(days=210) > pd.to_datetime(AF['STATPERS'])]
   AF_new = AF_new.drop_duplicates(['CUSIP', 'FPEDATS'], keep='last')

   #添加AF的FYEAR(calender year to fiscal year)
   def apply(x):
      if x.month < 4:
         return x.year - 1
      else:
         return x.year
   AF_new['FYEAR'] = AF['FPEDATS'].apply(func=apply)
   
   #merge AF and data_link (link IBES and COMP)
   AF_new = pd.merge(AF_new, data_link, left_on='TICKER', right_on='ibtic')
   AF_new.rename(columns={'CUSIP': 'CUSIP_8', 'cusip': 'CUSIP_9'}, inplace=True)
   AF_new.drop_duplicates(['TICKER', 'FYEAR'], keep='last', inplace=True)
   AF_new.to_csv(config.af_new, index=False)


def gen_comp():
   data1 = pd.read_csv(config.data1)
   data2 = pd.read_csv(config.data2)
   data3 = pd.read_csv(config.data3)
   data4 = pd.read_csv(config.data4)

   middle = pd.merge(data1, data2, on=['gvkey', 'datadate'])
   middle1 = pd.merge(data3, data4, on=['gvkey', 'datadate'])
   comp = pd.merge(middle, middle1, on=['gvkey', 'datadate'])
   comp.drop_duplicates(['gvkey', 'datadate'], keep='last', inplace=True)

   # build EARNINGS feature
   comp['spi'].fillna(0, inplace=True)
   comp['dvc'].fillna(0,inplace=True)
   comp['earnings'] = comp['ib'] - comp['spi'] * 0.65
   comp['E'] = comp['earnings'] / comp['csho'] #E earnings per share
   comp['DIV'] = comp['dvc'] / comp['csho']
   comp.replace([np.inf, -np.inf], np.nan, inplace=True)

   #comp_data是所有comp数据库中的数据合集
   key_variables = pd.read_csv(config.key_variables)
   comp_data = pd.merge(comp, key_variables, on=['gvkey', 'datadate'])
   comp_data.drop_duplicates(['gvkey','datadate','cusip','fyear'],keep='last',inplace=True)
   comp_data.rename(columns={'cusip':'CUSIP_9','fyear':'fyear_t_1'}, inplace=True)
   comp_data.to_csv(config.comp_data, index=False)
   
#build CF_data
def gen_feature():
    
    comp_data = pd.read_csv(config.comp_data)
    comp_data.dropna(inplace=True)

    #NEGE negative earnings indicator
    def NEGE(number):
        if number < 0:
            return 1
        else:
            return 0
    comp_data['NEGE'] = comp_data['E'].apply(NEGE)

    #DD non-dividend indicator
    def DD(number):
        if number > 0:
            return 0
        else:
            return 1
    comp_data['DIV'].fillna(0)
    comp_data['DD'] = comp_data['DIV'].apply(DD)

    #BTM = book values scaled by market value of equity
    comp_data['BTM'] = comp_data['ceq']/(np.multiply(np.abs(comp_data['prcc_f']), comp_data['csho']))
    comp_data['accruals_nochange'] = comp_data['act'] + comp_data['dlc'] - comp_data['che'] - comp_data['lct']
    #per-share
    comp_data['ac_nochange'] = comp_data['accruals_nochange'] / comp_data['csho']
    comp_data.dropna(inplace=True)
    #total asset per share
    comp_data['at_ps'] = comp_data['at'] / comp_data['csho']
    comp_data.replace([np.inf, -np.inf], np.nan,inplace=True)
    comp_data.dropna(inplace=True)

    #merge AF_data and comp_data(pay attention to time series)
    AF_new = pd.read_csv(config.af_new)
    AF_new['fyear_t_1'] = AF_new['FYEAR'] - 1
    E_y = comp_data[['gvkey', 'fyear_t_1', 'E']]
    E_y['fyear_t_1'] = E_y['fyear_t_1'] - 1
    E_y.rename(columns={'E':'RE'}, inplace=True) #RE is eps of year t+1
    middle2 = pd.merge(comp_data, AF_new, on=['gvkey','CUSIP_9','fyear_t_1'])
    CF_AF = pd.merge(middle2, E_y, on=['gvkey','fyear_t_1'])
    #build ag
    def rolling_aply(x):
       return (x[1] - x[0]) / x[0]

    def apply(x):
       x_ = x.rolling(window=2).apply(func=rolling_aply)
       return x_
    CF_AF['ag'] = CF_AF.groupby(['gvkey'])['at'].apply(func=apply)
    #build ACC
    CF_AF['ACC'] = CF_AF['ac_nochange'].diff()
    #ACC+ ACC-
    def ACC_P(number):
        if number >= 0:
            return number
        else:
            return 0
    CF_AF['ACC_P'] = CF_AF['ACC'].apply(ACC_P)
    CF_AF['ACC_P'].fillna(0,inplace=True)
    
    def ACC_N(number):
        if number < 0:
            return number
        else:
            return 0
    CF_AF['ACC_N'] = CF_AF['ACC'].apply(ACC_N)
    CF_AF['ACC_N'].fillna(0,inplace=True)
    
    #build e_p
    def E_p(number):
        if number >= 0:
            return number
        else:
            return 0
    CF_AF['E_p'] = CF_AF['E'].apply(E_p)
    
    CF_AF.replace([np.inf, -np.inf], np.nan, inplace=True)
    CF_AF.dropna(inplace=True)
    CF_AF.to_csv(config.cf_af, index=False)
    
def whole_table():
    data5 = pd.read_csv(config.data5,parse_dates=['date'])
    data5.rename(columns={'CUSIP':'CUSIP_8'}, inplace=True)
    data5['SHROUT'] = data5['SHROUT'] * 1000  #number of shares outstanding recorded in thousands
    
    CF_AF = pd.read_csv(config.cf_af,parse_dates=['datadate'])
    middle3 = pd.merge(CF_AF,data5,on='CUSIP_8')
    #monthly data 只需要t+1年底前七个月月底的数据
    middle3 = middle3[pd.to_datetime(middle3['datadate']) - datetime.timedelta(days=210) > pd.to_datetime(middle3['date'])]
    middle3 = middle3.drop_duplicates(['CUSIP_8','datadate'],keep='last')
    
    #builf share_aj
    grouped = middle3.groupby('gvkey')
    share_ajs = []
    gvkeys = []
    datadates = []
    for name,group in grouped:
        gvkey = group['gvkey']
        datadate = group['datadate']
        csho = group['csho']*1000000
        SHROUT = group['SHROUT']
        cs = list(csho)
        cs.insert(1,np.inf)
        cs.pop(-1)        
        share_aj = cs/SHROUT
        share_ajs.extend(share_aj)
        gvkeys.extend(gvkey)
        datadates.extend(datadate)
    dic_a = {'gvkey':gvkeys,'datadate':datadates,'share_aj':share_ajs}
    middle4 = pd.DataFrame(dic_a)
    middle4.replace([np.inf, -np.inf], np.nan, inplace=True)
    middle4.fillna(method='bfill',inplace=True)
          
    whole_data = pd.merge(middle3,middle4,on=['gvkey','datadate'])
    whole_data.to_csv(config.whole_data,index=False)

if __name__ == '__main__':
   # gen_AF()
   # gen_comp()
   gen_feature()