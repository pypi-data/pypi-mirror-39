# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 13:26:32 2018

@author: yili.peng
"""

from datetime import datetime

def change_index(df):
    convert=lambda x : datetime.strptime(x,'%Y%m%d')
    new_inx=[convert(str(x)) for x in df.index]
    df_new=df.copy()
    df_new.index=new_inx
    return df_new
