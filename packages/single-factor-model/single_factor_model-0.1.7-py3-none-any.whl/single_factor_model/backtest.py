# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:30:50 2018

@author: yili.peng
"""

import pandas as pd
#import os
from joblib import Parallel,delayed
from multiprocessing import Pool
from .global_func import seperate,portfolio_pct_change

def back_test_core(X):
    n,price,sus,ind,ind_weight,factor,factor_name,double_side_cost = X
    returns = price.pct_change()
    
    ports=['p%d'%i for i in range(n)]
    times=factor.index
    tickers=factor.columns
    m=len(times)
    # check availability
    if len(times)==0 or len(tickers)==0:
        raise Exception('wrong shape of input') 
        
    # initialize
    weight_list=[]
    portfolio_weight=pd.DataFrame(0,index=tickers,columns=ports).rename_axis('ticker').rename_axis('portfolio',axis=1)
    portfolio_vacant=pd.Series(1000,index=ports)
    portfolio_value=portfolio_vacant.rename(times[0]).to_frame().T.rename_axis('dt').rename_axis('portfolio',axis=1)
    portfolio_turnover=pd.Series(0,index=ports).rename(times[0]).to_frame().T.rename_axis('dt').rename_axis('portfolio',axis=1)
    
    if m==1:
        return portfolio_value

    for i in range(1,m):

        t_1=times[i-1]
        t=times[i]

        # freeze (t)
        # cannot close position
        port_sus=pd.DataFrame([sus.loc[t].eq(1)]*n,index=ports).T
        portfolio_freezer=portfolio_weight.where(port_sus).fillna(0)
        
        # change position (t)
        ## new weight
        ava_sample=pd.concat([factor.loc[t_1].rename('Factor')
                        ,ind.loc[t].rename('Industry')
                        ,sus.loc[t].rename('Suspend')]
                        ,axis=1).dropna(axis=0).query('Suspend==0')
        ava_ind=ind_weight.loc[t_1]\
                            .loc[ava_sample['Industry'].unique()]
        
        if ava_ind.shape[0]>0:
            # exists valid tickers and factor values
            if ava_ind.sum()>0:
                # valid industries are in index
                ava_ind_weight=ava_ind/ava_ind.sum()
            else:
                # valid industries aren't in index
                ava_ind_weight=pd.Series(1/ava_ind.shape[0],index=ava_ind.index)
            ava_weights=[]
            for industry,weight_of_ind in ava_ind_weight.items():
                tickers_of_ind=ava_sample.query('Industry==%s'%str(industry)).sort_values(by='Factor',ascending=False).index.tolist()
            #    port_weights_of_ind=seperate(tickers_of_ind,n).rename(index={i:'p'+str(i) for i in range(n)})*weight_of_ind
                port_weights_of_ind=seperate(tickers_of_ind,n).rename(index={i:'p'+str(i) for i in range(n)})*weight_of_ind
                ava_weights.append(port_weights_of_ind)
            new_portfolio_weight=pd.concat(ava_weights,axis=1).T
        else:
            new_portfolio_weight=portfolio_weight
            
        # redistribute weight
        unfrozen_weight=new_portfolio_weight.sum()-portfolio_freezer.sum()
        portfolio_weight2=new_portfolio_weight.mul(unfrozen_weight).add(portfolio_freezer,fill_value=0)
        
        # valuate (t)
        # portfolio_weight before changing position 
        ret=returns.loc[t].fillna(0)
        new_value=portfolio_value.loc[t_1]\
                            .mul(
                                portfolio_weight.mul(ret.add(1),axis=0).sum()
                                )\
                            .rename(t)
                            
        if portfolio_weight.sum().sum()==0:
            # hold no position
            new_value+=portfolio_vacant

        weight_diff=portfolio_pct_change(portfolio_weight,portfolio_weight2).rename(t)
        
        portfolio_value=portfolio_value.append(new_value*(1-weight_diff.mul(double_side_cost)))
        portfolio_turnover=portfolio_turnover.append(weight_diff)
        # update portfolio weight
        portfolio_weight=portfolio_weight2
        
        weight_list.append(portfolio_weight.unstack().rename(t))

    return portfolio_value.unstack().rename(factor_name),portfolio_turnover.unstack().rename(factor_name),pd.concat(weight_list,axis=1).rename_axis('dt',axis=1).stack().rename(factor_name)


def output_weight(Weight,weight_path,ind,ind_weight,sus,fac):
    
    if weight_path is None:
        return
#    if not os.path.exists(weight_path):
#        os.makedirs(weight_path)
    for f in Weight.columns:
        
        weight_df=Weight[f].unstack(level=0).swaplevel(axis=0).sort_index(axis=0).mul(100)
        
        Sus=sus.stack().rename('sus').reindex(weight_df.index)
        
        ind_df=ind.stack().rename('ind').reset_index()
        ind_weight_df=ind_weight.stack().rename('ind_weight').reset_index()
        Industry=pd.merge(ind_df,ind_weight_df,on=['dt','ind'],how='outer').set_index(['dt','ticker']).reindex(weight_df.index)
        
        Fac=fac[f].shift().stack().rename(f).reindex(weight_df.index)
        
        print('Write factor detail {}'.format(f))
        
        pd.concat([Fac,Industry,Sus,weight_df],axis=1)\
                .reset_index()\
                .sort_values(by=['dt','ind',f],ascending=[True,True,False])\
                .to_csv(weight_path,index=False,float_format='%.5f')
    return


def run_back_test(data_box,n=5,back_end=None,n_jobs=-1,factor_pool=None,weight_path=None,double_side_cost=0.003,**kwargs):
    '''
    data_box: data box class (compiled)
    n: number of portfolios. p_0 has the largest factor exposure while p_n has the least factor exposure.
    back_end: None/loky/multiprocessing
    factor_pool: subset of factors to run back test
    n_jobs: prossesors to run parallel algorithm. Valid when back end is not None.
    weight_path: defualt None. No output. 
    double_side_cost: transaction cost.
    '''
    if back_end is None:
        value_list,turnover_list,weight_list=[],[],[]
        for f in data_box.Factor.columns.levels[0]:
            print('Process factor {} with single processor'.format(f))
            X=(n,data_box.Price,data_box.Sus,data_box.Ind,data_box.Ind_weight,data_box.Factor.xs(f,axis=1),f,double_side_cost)
            BT_value,BT_turnover,BT_weight=back_test_core(X)
            # BT_value index: portfolio > time. value: values
            # BT_weight index: portfolio > ticker > time  value: weights
            value_list.append(BT_value)
            turnover_list.append(BT_turnover)
            weight_list.append(BT_weight)
    else:
        if back_end is 'loky':
            mul_res=Parallel(n_jobs=n_jobs,**kwargs)(
                    delayed(back_test_core)( (n,data_box.Price,data_box.Sus,data_box.Ind,data_box.Ind_weight,data_box.Factor.xs(f,axis=1),f,double_side_cost)
                                            ) for f in data_box.Factor.columns.levels[0])
        elif back_end is 'multiprocessing':
            X=[(n,data_box.Price,data_box.Sus,data_box.Ind,data_box.Ind_weight,data_box.Factor.xs(f,axis=1),f,double_side_cost) for f in data_box.Factor.columns.levels[0]]
            pool=Pool(processes=n_jobs,**kwargs)            
            mul_res=pool.map(back_test_core,X)
            pool.close()
            pool.join()
        else:
            raise Exception('wrong backend type')
        
        value_list,turnover_list,weight_list=[],[],[]
        for res in mul_res:
            value_list.append(res[0])
            turnover_list.append(res[1])
            weight_list.append(res[2])
        
    Value=pd.concat(value_list,axis=1)
    Turnover=pd.concat(turnover_list,axis=1)
    Weight=pd.concat(weight_list,axis=1)
    output_weight(Weight,weight_path,data_box.Ind,data_box.Ind_weight,data_box.Sus,data_box.Factor)
    return Value,Turnover

