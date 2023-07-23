# -*- coding: utf-8 -*-
import pandas as pd


from ipylib.idebug import *




class MemoryDB(object):

    def __init__(self, data):
        self.data = data 
    def get_frame(self): return pd.DataFrame(self.data)
    def show(self):
        print(self.get_frame())
    def search(self, **kwargs):
        df = self.get_frame()
        for k, v in kwargs.items():
            TF = df[k].str.contains(v, regex=True, na=False)
            df = df[TF]

        logger.info({'ResultLen': len(df)})
        return df.to_dict('records')