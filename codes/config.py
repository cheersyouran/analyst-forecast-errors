import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)
sys.path.append(rootPath)


class Config:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
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


config = Config()
