This programme is to automatically generate alpha factors

Dependencies
------------

-  python >= 3.5
-  pandas >= 0.22.0
-  numpy >= 1.14.0
-  RNWS >= 0.1.1
-  numba >= 0.38.0
-  single_factor_model>=0.1.5

Sample
------

load packages and read in data
==============================

.. code:: bash

   from alpha_factory import generator_class,get_memory_use_pct,clean
   from RNWS import read
   import numpy as np
   import pandas as pd
   start=20180101
   end=20180331
   factor_path='.'
   frame_path='.'

   df=pd.read_csv(frame_path+'/frames.csv')

   # read in data
   exr=read.read_df('./exr',file_pattern='exr',start=start,end=end)
   cap=read.read_df('./cap',file_pattern='cap',header=0,dat_col='cap',start=start,end=end)
   open_price,close,vwap,adj,high,low,volume,sus=read.read_df('./mkt_data',file_pattern='mkt',start=start,end=end,header=0,dat_col=['open','close','vwap','adjfactor','high','low','volume','sus'])
   ind1,ind2,ind3=read.read_df('./ind',file_pattern='ind',start=start,end=end,header=0,dat_col=['level1','level2','level3'])
   inx_weight=read.read_df('./ZZ800_weight','Stk_ZZ800',start=start,end=end,header=None,inx_col=1,dat_col=3)

Note:\ ``frames`` contains columns as:
``df_name,equation,dependency,type``, where ``type`` includes
``df,cap,group``. In this case ``frames.csv`` have ``df_name``:
``re,cap,open_price,close,vwap,high,low,volume,ind1,ind2,ind3``

start to generate
=================

.. code:: bash

   parms={'re':close.mul(adj).pct_change()
          ,'cap':cap
          ,'open_price':open_price
          ,'close':close
          ,'vwap':vwap
          ,'high':high
          ,'low':low
          ,'volume':volume
          ,'ind1':ind1
          ,'ind2':ind2
          ,'ind3':ind3}

   with generator_class(df,factor_path,**parms) as gen:
       gc.generator(batch_size=3,name_start='a')
       gc.generator(batch_size=3,name_start='a')
       gc.output_df(path=frame_path+'/frames_new.csv')

continue to generate with existing frames and factors
=====================================================

.. code:: bash

   with generator_class(df,factor_path,**parms) as gc:
       gc.reload_df(path=frame_path+'/frames_new.csv')
       gc.reload_factors()
       clean()
       for i in range(5):
           gc.generator(batch_size=2,name_start='a')
           print('step %d memory usage:\t %.1f%% \n'%(i,get_memory_use_pct()))
           if get_memory_use_pct()>80:
               break
       gc.output_df(path=frame_path+'/frames_new2.csv')

backtesting after generation
============================

.. code:: bash

   data_box_param={'ind':ind1
               ,'price':vwap*adjfactor
               ,'sus':sus
               ,'ind_weight':inx_weight
               ,'path':'./databox'
               }

   back_test_param={'sharpe_ratio_thresh':3
                    ,'n':5
                    ,'out_path':'.'
                    ,'back_end':'loky'
                    ,'n_jobs':6
                    ,'detail_root_path':None
                    ,'double_side_cost':0.003
                    ,'rf':0.03
                    }
   with generator_class(df,factor_path,**parms) as gen: 
       for i in range(5):
           gen.generator(batch_size=2,name_start='a')
           gen.output_df(path=frame_path+'/frames_new.csv')
           gen.create_data_box(**data_box_param)
           gen.back_test(**back_test_param)
           clean()
           if get_memory_use_pct()>90:
               print('Memory exceeded')
               break


