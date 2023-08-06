# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 15:57:44 2018

@author: yili.peng
"""

import empyrical as em
import pandas as pd
from joblib import Parallel,delayed
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os

def win_rate(Return):
    return 1-Return.le(0).mean()

def calc_basics(Return,name,annual_risk_free=0.03):
    risk_free=annual_risk_free/252
    return pd.DataFrame([em.annual_return(Return).values,
                         em.max_drawdown(Return).values,
                         em.sharpe_ratio(Return,risk_free=risk_free),
                         em.sortino_ratio(Return,required_return=risk_free).values,
                         win_rate(Return).values
                         ]
                        ,columns=Return.columns
                        ,index=pd.Index(['Annual_Return','Max_Drawndown','Sharpe_Ratio','Sortino_Ratio','Win_Rate'],name='stats')
                        ).unstack().rename(name)

def summary_core(X):
    Return,factor_name,annual_risk_free=X
    Return['long_short']=Return.iloc[:,0]-Return.iloc[:,-1]
    result=[calc_basics(Return,'total',annual_risk_free)]
    for key,group in Return.groupby(by=[Return.index.year,Return.index.month]):
        name=str(key[0]*100+key[1])
        result.append(calc_basics(group,name,annual_risk_free))
    return pd.concat(result,axis=1).rename_axis('period',axis=1).stack().rename(factor_name)

def summary_core_total(X):
    Return,factor_name,annual_risk_free=X
    Return['long_short']=Return.iloc[:,0]-Return.iloc[:,-1]
    return calc_basics(Return,factor_name,annual_risk_free)
    
def summary(Value,annual_risk_free=0.03,back_end=None,n_jobs=-1,**kwargs):
    '''
    Value: Value from run_back_test
    annual_risk_free: annualized risk free rate. Default 0.03.
    back_end: None/loky/multiprocessing
    n_jobs: prossesors to run parallel algorithm. Valid when back end is not None.
    '''
    assert back_end in (None,'loky','multiprocessing'),'wrong backend type'
    if back_end is None:
        lst=[]
        for f in Value.columns:
            Return=Value[f].unstack(level=0).pct_change().fillna(0)
            lst.append(summary_core((Return,f,annual_risk_free)))
    elif back_end is 'loky':
        lst=Parallel(n_jobs=n_jobs,**kwargs)(
                    delayed(summary_core)( (Value[f].unstack(level=0).pct_change().fillna(0),f,annual_risk_free) 
                                        ) for f in Value.columns)
    else:
        X=[(Value[f].unstack(level=0).pct_change().fillna(0),f,annual_risk_free) for f in Value.columns]
        pool=Pool(processes=n_jobs,**kwargs)            
        lst=pool.map(summary_core,X)
        pool.close()
        pool.join()
    summarized=pd.concat(lst,axis=1).rename_axis('factor',axis=1).stack().rename('value').reset_index().sort_values(['factor','period','stats','portfolio']).reindex(['factor','period','stats','portfolio','value'],axis=1)
    return summarized

def summary_total(Value,annual_risk_free=0.03,back_end=None,n_jobs=-1,**kwargs):
    
    assert back_end in (None,'loky','multiprocessing'),'wrong backend type'
    if back_end is None:
        lst=[]
        for f in Value.columns:
            Return=Value[f].unstack(level=0).pct_change().fillna(0)
            lst.append(summary_core_total((Return,f,annual_risk_free)))        
    elif back_end is 'loky':
        lst=Parallel(n_jobs=n_jobs,**kwargs)(
                    delayed(summary_core_total)( (Value[f].unstack(level=0).pct_change().fillna(0),f,annual_risk_free)
                                                ) for f in Value.columns)
    else:
        X=[(Value[f].unstack(level=0).pct_change().fillna(0),f,annual_risk_free) for f in Value.columns]
        pool=Pool(processes=n_jobs,**kwargs)            
        lst=pool.map(summary_core,X)
        pool.close()
        pool.join()
    summarized=pd.concat(lst,axis=1).rename_axis('factor',axis=1).stack().rename('value').reset_index().sort_values(['factor','stats','portfolio']).reindex(['factor','stats','portfolio','value'],axis=1)
    return summarized


def run_plot(Value,reference_value=None,save_path=None,show=False):
    '''
    reference_value: pd.Series with index as dt
    '''
    assert (reference_value is None) or (type(reference_value) is pd.Series), 'Wrong type of reference value' 
    
    for f in Value.columns:
        Return=Value[f].unstack(level=0).pct_change().fillna(0)
        long_short=(Return.iloc[:,0]-Return.iloc[:,-1]).add(1).cumprod()
        V=Return.add(1).cumprod()
        
        plt.style.use('ggplot')
        plt.figure(figsize=(18,10),dpi=100)   
        plt.plot(V)
        plt.fill_between(long_short.index,1,long_short,color='cornsilk',label='long short (p0 - p4)')
        if reference_value is None:
            plt.legend(list(V.columns)+['long short (p0 - p4)'],loc='best',fontsize=11)
        else:
            plt.plot(reference_value.reindex(long_short.index).pct_change().add(1).cumprod(),label='Index')
            plt.legend(list(V.columns)+['Index','long short (p0 - p4)'],loc='best',fontsize=11)
        plt.title(f)
        plt.gcf().autofmt_xdate()
        if save_path is not None:
            plt.savefig(os.path.join(save_path,f+'.png'))
        if show:
            plt.show()
        else: 
            plt.close('all')

def run_plot_turnover(Turnover,save_path=None,show=False):
    for f in Turnover.columns:
        V=Turnover[f].unstack(level=0)
        plt.style.use('ggplot')
        plt.figure(figsize=(18,10),dpi=100)   
        plt.plot(V)
        plt.title(f)
        plt.legend(V,loc='best',fontsize=11)
        plt.gcf().autofmt_xdate()        
        if save_path is not None:
            plt.savefig(os.path.join(save_path,f+'.png'))
        if show:
            plt.show()
        else: 
            plt.close('all')