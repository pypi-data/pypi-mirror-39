# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:39:21 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
from plotly.figure_factory import create_gantt
from datetime import datetime

from .cprint import cprint
from .change_index import change_index

class Account:
    def __init__(self,start_amount=1000):
        self.bank=start_amount
        self.total_value=start_amount
        self.stock=0.0
        self.history_bank=pd.Series()
        self.history_value=pd.Series()
        self.history_stock=pd.Series()
    def join_account(self,account2):
        self.bank+=account2.bank
        self.total_value+=account2.total_value
        self.stock+=account2.stock
        self.history_bank+=account2.history_bank
        self.history_value+=account2.history_value
        self.history_stock+=account2.history_stock
    def buy(self,amount):        
        if self.bank<amount:
            cprint('do not have enough money to buy',c='r',f='')
            return
        assert pd.isna(amount)==False,'Account.buy() amount is nan'
        self.bank-=amount
        self.stock+=amount
    def check_bank(self):
        return self.bank
    def check_stock(self):
        return self.stock
    def sell(self,amount):
        '''
        short allowed
        '''
        assert pd.isna(amount)==False,'Account.sell() amount is nan'
        self.bank+=amount
        self.stock-=amount
    def close_all_stock(self):
        self.bank+=self.stock
        self.stock=0.0
    def check_value(self):
        assert (pd.isna(self.bank) or pd.isna(self.stock) or pd.isna(self.total_value)) == False ,'Na value exists in account'
    def hold(self,new_stock_amount,daily_bank_rate=0):
        assert pd.isna(new_stock_amount)==False,'Account.hold() amount is nan'
        
        self.bank*=(1+daily_bank_rate)
        self.stock=new_stock_amount
        self.total_value=self.bank+self.stock
        
    def is_alive(self):
        return not((self.bank<0) or (self.total_value<0))
    def record(self,date):
        self.history_stock.at[date]=self.stock
        self.history_bank.at[date]=self.bank
        self.history_value.at[date]=self.total_value
    def plot_history(self,start=None,end=None,by_pct=False):
        start=(self.history_value.index.min() if start is None else start)
        end=(self.history_value.index.max() if end is None else end)
        plt.style.use('seaborn')
        fig =plt.figure(num=1,figsize=(12,8),dpi=100)
        
        ax0 = fig.add_subplot(211)
        if not by_pct:
            ax0.plot(change_index (self.history_value.loc[start:end]),label='history value')
        else:
            ax0.plot(change_index (self.history_value.loc[start:end]/self.history_value.loc[start:end].iloc[0]),label='history value')
        ax0.legend(loc=(0.02,0.80))
        ax1 = fig.add_subplot(212)
        ax1.plot(change_index (self.history_bank.loc[start:end]),linestyle='--',color='#4A7EBB',label='history bank')
        ax2 = ax1.twinx()  # this is the important function
        ax2.plot(change_index (self.history_stock.loc[start:end]),linestyle='--',color='#BE4B48',label='history stock')
        ax1.legend(loc=(0.02,0.78))
        ax2.legend(loc=(0.02,0.84))
        plt.gcf().autofmt_xdate()
        plt.show()
    def plot_history_add_index(self,index,start=None,end=None,by_pct=False):
        start=(self.history_value.index.min() if start is None else start)
        end=(self.history_value.index.max() if end is None else end)
        plt.style.use('seaborn')
        fig =plt.figure(num=1,figsize=(12,8),dpi=100)
        if not by_pct:
            ax0 = fig.add_subplot(211)
            ax0.plot(change_index (self.history_value.loc[start:end]),color='#BE4B48',label='history value')
            ax0.legend(loc=(0.02,0.84))
            ax3=ax0.twinx()
            ax3.plot(change_index (index.loc[start:end]),color='#4A7EBB',label='index value')
            ax3.legend(loc=(0.02,0.78))
        else:
            ax0 = fig.add_subplot(211)
            ax0.plot(change_index (self.history_value.loc[start:end]/self.history_value.loc[start:end].iloc[0]),color='#BE4B48',label='history value')
            ax0.plot(change_index (index.loc[start:end]/index.loc[start:end].iloc[0]),color='#4A7EBB',label='index value')
            ax0.legend(loc=(0.02,0.78))
        ax1 = fig.add_subplot(212)
        ax1.plot(change_index (self.history_bank.loc[start:end]),linestyle='--',color='#4A7EBB',label='history bank')
        ax2 = ax1.twinx()
        ax2.plot(change_index (self.history_stock.loc[start:end]),linestyle='--',color='#BE4B48',label='history stock')
        ax1.legend(loc=(0.02,0.78))
        ax2.legend(loc=(0.02,0.84))
        plt.gcf().autofmt_xdate()
        plt.show()
    def profit_list(self):
        '''
        trading periods' performance
        one trading period is defined from history_stock=0 to history_stock!=0 and return to history_stock=0 
        '''
        inx_start=None
        p=[]
        for inx in self.history_stock.index:
            i=self.history_stock.loc[inx]
            if (i==0) and (inx_start is not None):
                profit=self.history_value.loc[inx]-self.history_value.loc[inx_start]
                p.append(profit)
                inx_start=None
            elif inx_start is None:
                inx_start=inx
        return p
    def frequency(self):
        p=self.profit_list()
        return len(p)
    def win_rate(self):
        p=self.profit_list()
        return np.mean(np.array(p)>0)
    def sharpe_ratio(self,start=None,end=None,rf=0):
        '''
        annual sharpe ratio
        '''
        start=(self.history_value.index.min() if start is None else start)
        end=(self.history_value.index.max() if end is None else end)
        value=self.history_value.loc[start:end]
        return (value.pct_change().dropna().mean()-(rf))/value.pct_change().dropna().std()*15.8745
    def draw_down(self,start=None,end=None):
        start=(self.history_value.index.min() if start is None else start)
        end=(self.history_value.index.max() if end is None else end)
        value=self.history_value.loc[start:end]
        dd=min([value.loc[i:].div(value.loc[i]).min() for i in value.index])-1
        return -dd
    def annual_return(self,start=None,end=None):
        start=(self.history_value.index.min() if start is None else start)
        end=(self.history_value.index.max() if end is None else end)
        value=self.history_value.loc[start:end]
        return (value.iloc[-1]/value.iloc[0])**(250/value.shape[0])-1
    def romad(self,start=None,end=None):        
        return self.annual_return(start=start,end=end)/self.draw_down(start=start,end=end)

class Log:
    def __init__(self):
        '''
        status: 1 alive, 0 - -9 close
        '''
        self.log=pd.DataFrame(columns=['id','type','ticker','position','open_price','current_price','returns','abs_returns','max_returns','min_returns','max_abs_returns','min_abs_returns','open_dt','close_dt','duration','period','status','mark']) # log of every trade
    def load_log(self,log_df):
        self.log=log_df
    def join_log(self,log2):
        l=log2.log.copy()
        l.id+=self.log.id.max()+1
        self.log=pd.concat([self.log,l],axis=0,ignore_index=True)
    def append(self,one_log):
        self.log=self.log.append(one_log,ignore_index=True)
    def open_position(self,ticker,position,current_price,dt,period=0,position_type='main',mark=''):
        log_tmp=pd.Series([(0 if pd.isna(self.log.id.max()) else self.log.id.max()+1) ,position_type,ticker,position,current_price,current_price,0,0,0,0,0,0,dt,dt,0,period,1,mark],\
                          index=['id','type','ticker','position','open_price','current_price','returns','abs_returns','max_returns','min_returns','max_abs_returns','min_abs_returns','open_dt','close_dt','duration','period','status','mark'])
        self.append(log_tmp)
    def open_position_dual(self,ticker,position,current_price,dt,period=0,position_type='dual',mark=''):
        '''
        same id as last position but different type,
        dual type can only be closed with its main type log closed
        '''
        log_tmp=pd.Series([self.log.id.iloc[-1],position_type,ticker,position,current_price,current_price,0,0,0,0,0,0,dt,dt,0,period,1,mark],\
                          index=['id','type','ticker','position','open_price','current_price','returns','abs_returns','max_returns','min_returns','max_abs_returns','min_abs_returns','open_dt','close_dt','duration','period','status','mark'])
        self.append(log_tmp)
    def close_ticker(self,ticker,close_status=0,close_dual=False):
        flag=(self.log['ticker']==ticker)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_duration(self,duration_thresh,close_status=0,close_dual=False):
        '''
        close tickers whose holding date is longer than dt_thresh
        ''' 
        flag=(self.log['duration']>=duration_thresh)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_lower_returns(self,return_lower_thresh,close_status=0,close_dual=False):
        '''
        close tickers whose returns <= return_lower_thresh
        '''
        flag=(self.log['returns']<=return_lower_thresh)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_upper_returns(self,return_upper_thresh,close_status=0,close_dual=False):
        '''
        close tickers whose returns >= return_upper_thresh
        '''
        flag=(self.log['returns']>=return_upper_thresh)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_lower_abs_returns(self,abs_return_lower_thresh,close_status=0,close_dual=False):
        '''
        close tickers whose abs returns <= abs_return_lower_thresh
        '''
        flag=(self.log['abs_returns']<=abs_return_lower_thresh)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_upper_abs_returns(self,abs_return_upper_thresh,close_status=0,close_dual=False):
        '''
        close tickers whose abs returns >= abs_return_upper_thresh
        '''
        flag=(self.log['abs_returns']>=abs_return_upper_thresh)&(self.log['status']==1)&(self.log['type']=='main')
        if close_dual:
            ids=self.log.loc[flag,'id'].tolist()
            flag=self.log['id'].isin(ids)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_lower_abs_returns_dual(self,abs_return_lower_thresh,close_status=0):
        flag=(self.log['status']==1)
        id_flag=self.log.loc[flag].groupby('id').agg({'abs_returns':sum})['abs_returns'].le(abs_return_lower_thresh)
        closed_ids=[self.close_id(idx,close_status=close_status) for idx in id_flag.index[id_flag]]
        if len(closed_ids)>0:
            return pd.concat(closed_ids,axis=0)
        else:
            return pd.DataFrame(columns=['id','type','ticker','position','open_price','current_price','returns','abs_returns','max_returns','min_returns','max_abs_returns','min_abs_returns','open_dt','close_dt','duration','period','status','mark'])
        
    def close_upper_abs_returns_dual(self,abs_return_lower_thresh,close_status=0):
        flag=(self.log['status']==1)
        id_flag=self.log.loc[flag].groupby('id').agg({'abs_returns':sum})['abs_returns'].ge(abs_return_lower_thresh)
        closed_ids=[self.close_id(idx,close_status=close_status) for idx in id_flag.index[id_flag]]
        if len(closed_ids)>0:
            return pd.concat(closed_ids,axis=0)
        else:
            return pd.DataFrame(columns=['id','type','ticker','position','open_price','current_price','returns','abs_returns','max_returns','min_returns','max_abs_returns','min_abs_returns','open_dt','close_dt','duration','period','status','mark'])        
    def close_id(self,log_id,close_status=0):
        flag=(self.log['id']==log_id)&(self.log['status']==1)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    def close_mark(self,mark,close_status=0):
        flag=(self.log['mark']==mark)&(self.log['status']==1)
        self.log.loc[flag,'status']=close_status
        return self.log.loc[flag]
    
    def returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'returns']=self.log.loc[flag,'current_price']\
                                            .div(self.log.loc[flag,'open_price'])\
                                            .sub(1)\
                                            .mul(np.sign(self.log.loc[flag,'position']))
    def abs_returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'abs_returns']=self.log.loc[flag,'current_price']\
                                            .sub(self.log.loc[flag,'open_price'])\
                                            .mul(self.log.loc[flag,'position'])
    def max_returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'max_returns']=self.log.loc[flag,['max_returns','returns']].max(axis=1)
    def min_returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'min_returns']=self.log.loc[flag,['min_returns','returns']].min(axis=1)
    def max_abs_returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'max_abs_returns']=self.log.loc[flag,['max_abs_returns','abs_returns']].max(axis=1)
    def min_abs_returns(self):
        flag=(self.log['status']==1)
        self.log.loc[flag,'min_abs_returns']=self.log.loc[flag,['min_abs_returns','abs_returns']].min(axis=1)        
    def hold(self,current_price,dt):
        '''
        current_price includes dual_price
        '''
        flag=(self.log['status']==1)
        self.log.loc[flag,'current_price']=current_price.reindex(self.log.loc[flag,'ticker']).values
        self.log.loc[flag,'duration']+=1
        self.log.loc[flag,'close_dt']=dt
        self.returns()
        self.abs_returns()
        self.max_returns()
        self.min_returns()
        self.max_abs_returns()
        self.min_abs_returns()
    def settle(self):
        self.delete_zero()
    def alive_amount(self,start=None,end=None):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        flag=(self.log['status']==1)&(self.log['open_dt']>=start)&(self.log['close_dt']<=end)
        return self.log.loc[flag,'current_price'].mul(self.log.loc[flag,'position']).sum()
    def alive_amount_by_ticker(self,ticker,start=None,end=None):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        flag=(self.log['status']==1)&(self.log['open_dt']>=start)&(self.log['close_dt']<=end)&(self.log['ticker']==ticker)
        return self.log.loc[flag,'current_price'].mul(self.log.loc[flag,'position']).sum()
    def alive_trade(self,start=None,end=None):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        return sum((self.log['status']==1)&(self.log['open_dt']>=start)&(self.log['close_dt']<=end))
    def total_trade(self,start=None,end=None,dual=False):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        flag=(self.log['open_dt']>=start)&(self.log['close_dt']<=end)
        if dual:
            return self.log.loc[flag].id.unique().shape[0]
        else:
            return self.log.loc[flag].shape[0]
    def pos_trade(self,start=None,end=None,dual=False):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        flag=(self.log['open_dt']>=start)&(self.log['close_dt']<=end)
        if not dual:
            return self.log.loc[flag].returns.ge(0).sum()
        else:
            return self.log.groupby('id').agg({'abs_returns':sum})['abs_returns'].ge(0).sum()
    def win_rate(self,start=None,end=None,dual=False):
        return self.pos_trade(start,end,dual)/self.total_trade(start,end,dual)
    def main_trade(self,trade_type='main',start=None,end=None):
        start=(self.log.open_dt.min() if start is None else start)
        end=(self.log.close_dt.max() if end is None else end)
        return (self.log.loc[(self.log['open_dt']>=start)&(self.log['close_dt']<=end),'type']==trade_type).sum()
    def delete_zero(self):
        flag=((self.log['status']!=1)&(self.log['duration']==0))|(self.log['position']==0)
        self.log=self.log[~flag]
    def plot_history_position(self):
        '''
        open your browser to show plot
        '''
        cap=lambda x: min(100,max(0,x))
        lst=[dict(Task=self.log.loc[inx,'ticker'],Start=datetime.strptime(str(self.log.loc[inx,'open_dt']),'%Y%m%d'),Finish=datetime.strptime(str(self.log.loc[inx,'close_dt']),'%Y%m%d'),Returns=cap((self.log.loc[inx,'returns']+0.2)*250)) for inx in self.log.index]
        fig = create_gantt(lst, colors=['rgb(0,255,0)','rgb(255,0,0)'], index_col='Returns', show_colorbar=True,group_tasks=True,bar_width=0.2, showgrid_x=True, showgrid_y=True)
        plot(fig)
    def check_trade_cost(self,per_trade=0.0008):
        flag=((self.log['status']!=1)&(self.log['duration']!=0))
        return self.log.loc[flag].eval('(open_price+current_price)*position').abs().sum()*per_trade
    def check_position_at_date(self,dt):
        flag=((self.log['open_dt']<=dt)&(self.log['close_dt']>=dt))
        return self.log.loc[flag].groupby('ticker').agg({'position':sum})

class Mini_Exchange:
    def __init__(self,price=None):
        self.price=price
        self.user_file={}
        self.main_user=None
        self.frozen_users=[]
    def set_price(self,price):
        self.price=price
    def update_price(self,new_price):
        '''
        new_price: pd.DataFrame or pd.Series
        '''
        self.price=self.price.append(new_price)
    def register(self,user_name,account,log):        
        self.user_file.update({user_name:[account,log]})
    def is_register(self,user_name):
        return (user_name in self.user_file)
    def delete_user(self,user_name):
        if self.is_register(user_name):
            self.user_file.pop(user_name)
    def freeze_user(self,user_name):
        if self.is_register(user_name):
            self.frozen_users.append(user_name)
    def set_main_user(self,user_name):
        if self.is_register(user_name):
            self.main_user=user_name
        else:
            cprint('no such user',c='r',f='')
    def long(self,ticker,amount,dt,user=None,period=0,position_type='main',mark=''):
        '''
        user=None refer to main user
        '''
        user = (self.main_user if user is None else user)
        if not self.is_register(user):
            cprint('no such user',c='r',f='')
        elif user in self.frozen_users:
            cprint('user frozen',c='r',f='')
        elif ((dt not in self.price.index)\
            or (ticker not in self.price.columns)\
            or (pd.isna(self.price.loc[dt,ticker]))\
            or (self.price.loc[dt,ticker]<=0)\
            or pd.isna(self.price.loc[dt,ticker])
            ):
            cprint('price of %s at %s is not validate'%(str(ticker),str(dt)),c='r',f='')
        else:
            acc,log=self.user_file[user]
            amt_bank=acc.check_bank()
            amt_to_buy=min(amount,amt_bank)
            acc.buy(amt_to_buy)
            if position_type == 'main':
                log.open_position(ticker,amt_to_buy/self.price.loc[dt,ticker],self.price.loc[dt,ticker],dt,period=period,position_type=position_type,mark=mark)
            else:
                log.open_position_dual(ticker,amt_to_buy/self.price.loc[dt,ticker],self.price.loc[dt,ticker],dt,period=period,position_type=position_type,mark=mark)
    def short(self,ticker,amount,dt,user=None,period=0,position_type='main',mark=''):
        user = (self.main_user if user is None else user)
        if not self.is_register(user):
            cprint('no such user',c='r',f='')
        elif user in self.frozen_users:
            cprint('user frozen',c='r',f='')
        elif ((dt not in self.price.index)\
            or (ticker not in self.price.columns)\
            or (pd.isna(self.price.loc[dt,ticker]))\
            or (self.price.loc[dt,ticker]<=0)\
            or pd.isna(self.price.loc[dt,ticker])
            ):
            cprint('price of %s at %s is not validate'%(str(ticker),str(dt)),c='r',f='')
        else:
            acc,log=self.user_file[user]
            acc.sell(amount)
            if position_type == 'main':
                log.open_position(ticker,-amount/self.price.loc[dt,ticker],self.price.loc[dt,ticker],dt,period,position_type=position_type,mark=mark)
            else:
                log.open_position_dual(ticker,-amount/self.price.loc[dt,ticker],self.price.loc[dt,ticker],dt,period,position_type=position_type,mark=mark)
    def close(self,dt,value,by='ticker',user=None,close_status=0,close_dual=False):
        '''
        by: 'ticker','duration','lower_return','upper_return','lower_abs_return','upper_abs_return','mark'
        value: corresponding value
        '''
        user = (self.main_user if user is None else user)
        if not self.is_register(user):
            cprint('no such user',c='r',f='')
        elif user in self.frozen_users:
            cprint('user frozen',c='r',f='')
        else:
            acc,log=self.user_file[user]
            if by=='ticker':
                closed_log=log.close_ticker(ticker=value,close_status=close_status,close_dual=close_dual)
            elif by=='duration':
                closed_log=log.close_duration(duration_thresh=value,close_status=close_status,close_dual=close_dual)
            elif by =='lower_return':
                closed_log=log.close_lower_returns(value,close_status=close_status,close_dual=close_dual)
            elif by =='upper_return':                
                closed_log=log.close_upper_returns(value,close_status=close_status,close_dual=close_dual)
            elif by =='lower_abs_return':
                closed_log=log.close_lower_abs_returns(value,close_status=close_status,close_dual=close_dual)
            elif by =='upper_abs_return':                
                closed_log=log.close_upper_abs_returns(value,close_status=close_status,close_dual=close_dual)
            elif by =='lower_abs_returns_dual':
                closed_log=log.close_lower_abs_returns_dual(value,close_status=close_status)
            elif by =='upper_abs_returns_dual':
                closed_log=log.close_upper_abs_returns_dual(value,close_status=close_status)
            elif by == 'mark':
                closed_log=log.close_mark(value,close_status=close_status)
            else:
                cprint('wrong value of by',c='r',f='')
                return
            if closed_log.shape[0]>0:
                closed_amt=sum(closed_log['position']*closed_log['current_price'])
                if closed_amt>=0:
                    acc.sell(closed_amt)
                else:
                    acc.buy(-closed_amt)
    def settle(self,dt):
        for user,files in self.user_file.items():
            if user not in self.frozen_users:
                acc,log=files
                acc.record(dt)
                log.settle()
    def hold(self,dt):
        if dt not in self.price.index:
            cprint('price at %s is not validate'%(str(dt)),c='r',f='')
        else:
            for user,files in self.user_file.items():
                if user not in self.frozen_users:
                    acc,log=files
                    log.hold(self.price.loc[dt],dt) 
                    acc.hold(new_stock_amount=log.alive_amount())
                    if not acc.is_alive():
                        cprint('account %s at %s is now closed out'%(str(user),str(dt)),c='r',f='')
                        self.freeze_user(user)