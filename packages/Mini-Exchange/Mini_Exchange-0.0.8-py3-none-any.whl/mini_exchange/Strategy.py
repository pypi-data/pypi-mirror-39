# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 10:39:41 2018

@author: yili.peng
"""
import pandas as pd
from .Trading_system import Account,Log,Mini_Exchange
from .cprint import cprint

class Strategy_Master:
    def __init__(self,price):
        self.price=price
        self.MM=Mini_Exchange(price)
        self.users={}
        self.close_strategies=[]
        self.open_strategies=['False']
    def add_user(self,user_name,signal,start_amount=1000):
        '''
        signal: Dataframe as  
                -- (period,dt) * tickers:
                with Value            
                    0 or nan or other number: hold still
                    1: long
                    2: close long position
                    3: close long and open short
                    -1: short
                    -2: close short position
                    -3: close short and open long
        '''
        acc=Account(start_amount=start_amount)
        log=Log()
        self.MM.register(user_name,account=acc,log=log)
        if not isinstance(signal.index,pd.core.index.MultiIndex):
            signal=pd.concat([signal],keys=[0])
  
        self.users.update({user_name:[signal,acc,log]})
        
    def trade_one(self,user_name,user_amt_srs,allow_short,dt):
        if dt not in self.users[user_name][0].index.levels[1][self.users[user_name][0].index.labels[1]]:
            return
        sub_signal=self.users[user_name][0].xs(dt,axis=0,level=1).iloc[0].fillna(0)
        period=sub_signal.name
        for ticker,sig in sub_signal[sub_signal!=0].items():
            if (sig==2):
                self.MM.close(dt=dt,value=ticker,by='ticker',close_status=0,user=user_name)
            elif allow_short and (sig==-2):
                self.MM.close(dt=dt,value=ticker,by='ticker',close_status=0,user=user_name)
            elif (sig==1):
                if not eval(' or '.join(self.open_strategies)):
                    amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                    self.MM.long(ticker,amount,dt,user=user_name,period=period)
            elif allow_short and (sig==-1) :
                if not eval(' or '.join(self.open_strategies)):
                    amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                    self.MM.short(ticker,amount,dt,user=user_name)
            elif (sig==3):
                self.MM.close(dt=dt,value=ticker,by='ticker',close_status=0,user=user_name)
                if allow_short:
                    if not eval(' or '.join(self.open_strategies)):
                        amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                        self.MM.short(ticker,amount,dt,user=user_name)
            elif (sig==-3):
                if allow_short:
                    self.MM.close(dt=dt,value=ticker,by='ticker',close_status=0,user=user_name)
                if not eval(' or '.join(self.open_strategies)):
                    amount=(user_amt_srs['value'] if user_amt_srs['amt_type']==0 else user_amt_srs['value']*self.users[user_name][1].total_value)
                    self.MM.long(ticker,amount,dt,user=user_name,period=period)
            else:
                continue

    def add_open_strategy(self,user_name,strategy_name,threshold_value=1):
        '''
        strategy_name: 'one_trade','amount_per_ticker','ratio_per_ticler'
        '''
        subline="(user_name=='%s')"%user_name
        if strategy_name == 'one_trade':
            subline+=' and (self.users[user_name][2].alive_amount_by_ticker(ticker)!=0)'
        elif strategy_name == 'amount_per_ticker':
            subline+=' and (abs(self.users[user_name][2].alive_amount_by_ticker(ticker))>=%s)'%str(threshold_value)
        elif strategy_name == 'ratio_per_ticler':
            subline+=' and (abs(self.users[user_name][2].alive_amount_by_ticker(ticker)/(self.users[user_name][1].total_value))>=%s)'%str(threshold_value)
        else:
            cprint('strategy name cannot be recognied',c='r',f='')
            return
        self.open_strategies.append('('+subline+')')
    def add_close_strategy(self,user_name,strategy_name,threshold_value,close_status=0):
        '''
        strategy_name: 'duration','lower_return','upper_return','lower_abs_return','upper_abs_return','upper_abs_returns_dual','lower_abs_returns_dual'
        '''
        if strategy_name in ('duration','lower_return','upper_return','lower_abs_return','upper_abs_return','upper_abs_returns_dual','lower_abs_returns_dual'):
            line="self.MM.close(dt,value=%s,by='%s',user='%s',close_status=%s)"%(str(threshold_value),strategy_name,user_name,str(close_status))
            self.close_strategies.append(line)
        else:
            cprint('strategy name cannot be recognied',c='r',f='')
    def trade(self,user_amt_df,allow_short=True):
        '''
        user_amt_df: Columns
                    -- user_name,amt_type,value
                    amt_type
                    -- 0 (by abs amt)
                    -- 1 (by rate of total value)
        allow_short: whether short sell is allowed
        '''
        for s in ('user_name','amt_type','value'):
            if s not in user_amt_df.columns:
                raise Exception('wrong type of user_amt_df')
        for dt in self.price.index:
            print('\rrun %d'%dt,end='\r')
            self.MM.hold(dt)
            for line in self.close_strategies:
                exec(line)
            for inx in user_amt_df.index:
                user=user_amt_df.loc[inx,'user_name']
                if user not in self.users:
                    continue
                else:
                    self.trade_one(user_name=user,user_amt_srs=user_amt_df.loc[inx],allow_short=allow_short,dt=dt)
            self.MM.settle(dt)
        print('')
    def get_user(self,user_name):
        return self.users[user_name][1],self.users[user_name][2]
    def summary(self,start=None,end=None):
        D={}
        kk=[]
        for key,lst in self.users.items():
            signal,acc,pos=lst
            D.update({key:[acc.annual_return(start,end),acc.sharpe_ratio(start,end),acc.romad(start,end),pos.win_rate(start,end),pos.total_trade(start,end),acc.draw_down(start,end)]})
            kk.append(key)
        R=pd.DataFrame(D,index=['annual_return','sharpe_ratio','romad','win_rate','total_trade','mad']).T
        with pd.option_context('display.max.columns',None):
            print('\nTotal Performance:\n')
            print(R.round(3).sort_values('annual_return',ascending=False))