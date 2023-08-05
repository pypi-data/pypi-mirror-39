This project is to simulate an exchange in order to bakc test quant
strategies.

Dependencies
~~~~~~~~~~~~

-  python 3.5
-  pandas 0.23.0
-  spyder 3.2.8
-  plotly 2.7.0

Installation
~~~~~~~~~~~~

.. code:: bash

   pip install mini_exchange

Usage
~~~~~

.. code:: bash

   # price: dataframe dt*ticker
   # signal01: dataframe dt*ticker
   # signal02: dataframe dt*ticker

   dates=price.loc[start:end].index
   tickers=price.columns

   from mini_exchange import Mini_Exchange,Account,Log
   MM=Mini_Exchange(price)
   # create user01
   acc01=Account(start_amount=1000)
   log01=Log()
   MM.register(user_name='user01',account=acc01,log=log01)
   # create user02
   acc02=Account(start_amount=1000)
   log02=Log()
   MM.register(user_name='user02',account=acc02,log=log02)
   # trade
   for dt in dates:
       print('\rrun %d'%dt,end='\r')
       MM.hold(dt)
       for ticker in tickers:
           #user01
           if signal01.loc[dt,ticker]==1: 
               #open long
               MM.long(ticker,amount=10,dt=dt,user='user01')
           elif signal01.loc[dt,ticker]==-1: 
               #open short
               MM.short(ticker,amount=10,dt=dt,user='user01')
           elif signal01.loc[dt,ticker].isin((-2,2)):
               #close
               MM.close(dt,ticker, by='ticker',user='user01')
           #user02
           if signal02.loc[dt,ticker]==1: 
               #open long
               MM.long(ticker,amount=10,dt=dt,user='user02')
           elif signal02.loc[dt,ticker]==-1: 
               #open short
               MM.short(ticker,amount=10,dt=dt,user='user02')
           elif signal01.loc[dt,ticker].isin((-2,2)):
               #close
               MM.close(dt,ticker, by='ticker',user='user01')
       MM.settle(dt)
   # summary
   # user01
   print(acc01.annual_return(),acc01.sharpe_ratio(rf=0.03))
   print(pos01.win_rate())
   acc01.plot_history(by_pct=True)
   pos01.plot_history_position()
   history_position=pos01.pos
   history_value=acc01.history_value


