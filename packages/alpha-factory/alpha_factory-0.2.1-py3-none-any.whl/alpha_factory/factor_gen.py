# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 16:32:58 2018

@author: yili.peng
"""

from .cprint import cprint
from .check_mem import clean
from .generator_core import generate_batch 
from single_factor_model import data_box,run_back_test,summary_total,run_plot,run_plot_turnover
from RNWS import read_df
import os
from glob import glob
import pandas as pd
import time
import warnings
warnings.simplefilter('ignore')

def find_dependency(df):
    return tuple(df.index[df['dependency'].isnull()])

def find_all_factors(path):
    pathlist=[[i,glob(i+'/factor_[0-9]*.csv')[1]] for i in glob(path+'/factor_part[0-9]*')]
    factor_list=[]
    for p in pathlist:
        line=open(p[1],'r').readline()
        factor_list.append([p[0],line.strip('\n').split(',')[1:]])
    return factor_list

def find_part(path):
    try:
        a=max([int(i[-3:]) for i in glob(path+'/*')])+1
    except:
        a=0
    return a

class generator_class:
    def __init__(self,df,factor_path,**parms):
        '''
        df: factor dataframe
        factor_path: root path to store factors
        **parms: all dependency dataframes
        '''
        flag=[i in parms.keys() for i in df.loc[df['dependency'].isnull(),'df_name']]
        if not all(flag):
            print('dependency:',find_dependency(df))
            raise Exception('need all dependencies')
        self.parms=parms
        self.df=df
        self.batch_num=find_part(factor_path)
        self.factor_path=factor_path
        self.d={}
        self.db=None
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    def reload_factors(self,**kwargs):
        factor_list=find_all_factors(self.factor_path)
        if len(factor_list)==0:
            pass
        else:
            for l in find_all_factors(self.factor_path):
                path=l[0]
                factors=l[1]
                print('reload: ',path)
                factor_exposures=read_df(path=path,file_pattern='factor',header=0,dat_col=factors,**kwargs)
                self.parms.update({factors[i]:factor_exposures[i] for i in range(len(factors))})
                self.d.update({factors[i]:factor_exposures[i] for i in range(len(factors))})
    def reload_df(self,path,**kwargs):
        self.df=pd.read_csv(filepath_or_buffer=path,**kwargs)
    def output_df(self,path,**kwargs):
        self.df.to_csv(path_or_buf=path,index=False,**kwargs)
    def generator(self,name_start='a',batch_size=50):
        '''
        multiprocessing is deprecated due to vast memory sharing problem
        '''
        cprint('\nGenerating one batch start',c='',f='l')
        t0=time.time()
        new_df,new_parms,d=generate_batch(self.df,batch_size=batch_size,out_file_path=self.factor_path+'/factor_part'+str(self.batch_num).zfill(3),name_start=name_start,**self.parms)
        self.parms.update(new_parms)
        self.df=new_df
        self.batch_num+=1
        t1=time.time()
        cprint('Generating one batch finished --- time %.3f s\n'%(t1-t0),c='',f='l')
        self.d=d
        new_df=new_parms=t0=t1=None
        clean()
    def create_data_box(self,price=None,ind=None,ind_weight=None,sus=None,path=None):
        '''
        path: None(default) or the path to save databox (and reload next time when this function is called).
        '''
        if path is None:
            cprint('\nCreating data box')
            assert isinstance(price,pd.DataFrame) and isinstance(ind,pd.DataFrame) and isinstance(ind_weight,pd.DataFrame) and isinstance(sus,pd.DataFrame),'please input dataframe'
            db=data_box()
            db.load_adjPrice(price)
            db.load_indestry(ind)
            db.load_indexWeight(ind_weight)
            db.load_suspend(sus)
            db.set_lag(freq='d',day_lag=0)
            self.db=db
        elif os.path.exists(path):
            cprint('\nLoading data box')
            db=data_box()
            db.load(path)
            self.db=db
        else:
            assert isinstance(price,pd.DataFrame) and isinstance(ind,pd.DataFrame) and isinstance(ind_weight,pd.DataFrame) and isinstance(sus,pd.DataFrame),'please input dataframe'
            db=data_box()
            db.load_adjPrice(price)
            db.load_indestry(ind)
            db.load_indexWeight(ind_weight)
            db.load_suspend(sus)
            db.set_lag(freq='d',day_lag=0)
            db.save(path)
            self.db=db
    def back_test(self,sharpe_ratio_thresh=3,n=5,out_path=None,back_end='loky',n_jobs=-1,detail_root_path=None,double_side_cost=0.003,rf=0.03):
        '''
        Before back_test, data_box must be created by function create_data_box
        '''
        out_path= os.path.join(self.factor_path,'..') if out_path is None else out_path
        
        for f,df in self.d.items():
            self.db.add_factor(f,df)
        self.db.compile_data()
        
        cprint('\nRun backtesting start')
        
        Value,Turnover=run_back_test(self.db,n=n,back_end=back_end,n_jobs=n_jobs,weight_path=detail_root_path,double_side_cost=double_side_cost)
        
        S=summary_total(Value,annual_risk_free=rf)
        
        SS=S.query('(stats=="Sharpe_Ratio")&(portfolio=="long_short")')[['factor','value']]
        chosen_factors=SS.query('(abs(value)>{})'.format(sharpe_ratio_thresh)).factor.tolist()
        
        cprint('\nRun backtesting end, output figures')
        
        run_plot(Value[chosen_factors],save_path=out_path+'/figure')
        run_plot_turnover(Turnover[chosen_factors],save_path=out_path+'/figure')
        
        output_s=os.path.join(out_path,'SS')
        if not os.path.exists(output_s):
            os.makedirs(output_s)      
        SS.to_csv(output_s+'/SS.csv',index=False,header=False,mode='a')
