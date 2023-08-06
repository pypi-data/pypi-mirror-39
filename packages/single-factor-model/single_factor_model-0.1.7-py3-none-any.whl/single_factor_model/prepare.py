# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:13:02 2018

@author: yili.peng
"""
from .global_func import pre_sus,change_index,monthmove,check_time
from datetime import datetime
import pandas as pd
from pandas.api.types import is_numeric_dtype
from functools import reduce
import pickle

class ci_transformer:
    def __init__(self):
        self.columns=None
        self.index=None
    def fit_columns(self,*args):
        a=list(reduce(lambda x,y: set(x)&set(y),[i.columns for i in args]))
        a.sort()
        self.columns=a
    def fit_index(self,*args):
        a=list(reduce(lambda x,y: set(x)&set(y),[i.index for i in args]))
        a.sort()
        self.index=a
    def fit(self,*args):
        self.fit_columns(*args)
        self.fit_index(*args)
    def transform_columns(self,*args):
        return [a.reindex(columns=self.columns) for a in args]
    def transform_index(self,*args):
        return [a.reindex(index=self.index) for a in args]
    def transform(self,*args):
        return [a.reindex(index=self.index,columns=self.columns) for a in args]


class data_box(object):
    def __init__(self):
        self._factorDF=None
        self._freq='d'
        self._day_lag=0
        self._period_lag=0
        self._fixed_date=None
        self._start_time=None
        self._end_time=None
        
        self._Factors={}
        self._suspend=None
        self._price=None
        self._industry=None
        self._industry_weight=None
        self._index_weight=None
        self._factorDF=None

    @property
    def Price(self):
        assert self._price is not None,'Load Price first'
        return self._price.loc[self._start_time:self._end_time]
    @property
    def Sus(self):
        assert self._suspend is not None,'Load Suspend first'
        return self._suspend.loc[self._start_time:self._end_time]
    @property
    def Ind(self):
        assert self._industry is not None,'Load Industry first'
        return self._industry.loc[self._start_time:self._end_time]
    @property
    def Ind_weight(self):
        assert self._industry_weight  is not None,'Load IndexWeight and compile first'
        return self._industry_weight.loc[self._start_time:self._end_time]
    @property
    def Index_weight(self):
        assert self._index_weight is not None,'Load IndexWeight first'
        return self._index_weight
    @property
    def Factor(self):
        if self._factorDF is None:
            assert len(self._Factors) is not 0,'Load Factor first'
            return pd.concat(self._Factors.values(),axis=1,keys=self._Factors.keys()).loc[self._start_time:self._end_time]
        else:
            return self._factorDF.loc[self._start_time:self._end_time]
        
    def set_lag(self,freq='d',period_lag=0,day_lag=0,fixed_date=None,**kwargs):
        '''
        freq: 'd'/'m' daily or monthly
        day_lag: int
            Lags between the factor exposure date (T) and the factor exposure calculated date (T+n).
            lag = 0 means factor can be used T+1 
        period_lag: int
            Lags between the factor exposure period (T) and the factor exposure calculated period (T+n)
            For freq='d', period_lag and  day_lag are the same, the max of these two would be used.
            But for freq='m', total lag is the plus of day_lag and period_lag
        fixed_date: int
            Fixed calulate date when freq = 'm', combined with period_lag and day_lag if set.
        '''
        
        assert freq.lower() in ('d','m'), 'freq must in "d" / "m"'
        assert (fixed_date is None) or (type(fixed_date) is int), 'fixed_date must be None or int'
        
        self._freq=freq
        if freq is 'd':
            self._day_lag=self._period_lag=max(period_lag,day_lag)
        else:
            self._day_lag=day_lag
            self._period_lag=period_lag
            self._fixed_date=fixed_date

    def set_time(self,start_time=None,end_time=None,**kwargs):
        '''  
        set time span
        '''
        self._start_time=(datetime.strptime(str(start_time),'%Y%m%d') if start_time is not None else None)
        self._end_time=(datetime.strptime(str(end_time),'%Y%m%d') if end_time is not None else None)

    def add_factor(self,factor_name,factor_df,change_index_to_date=True,factor_pool=None,**kwargs):
        '''
        factor_name: str
        factor_df: DataFrame (times*tickers). Monthly factor should be have only one index each month
        factor_pool: Pool of factors to be included. Default None (all)
        '''
        if (factor_pool is None) or (factor_name in factor_pool):
            assert factor_df.apply(is_numeric_dtype).all(), 'Factor DataFrame contains Non-numeric type'
            
            
            self._Factors[factor_name]=(change_index(factor_df) if change_index_to_date else factor_df)
        
    def load_adjPrice(self,price_df,change_index_to_date=True,**kwargs):
        
        assert price_df.apply(is_numeric_dtype).all(), 'Open DataFrame contains Non-numeric type'
        self._price=(change_index(price_df) if change_index_to_date else price_df)
        
    def load_suspend(self,suspend_df,change_index_to_date=True,**kwargs):
        
        assert suspend_df.apply(is_numeric_dtype).all(), 'Suspend DataFrame contains Non-numeric type'
        suspend_df2=suspend_df.astype(int).apply(pre_sus)
        self._suspend=(change_index(suspend_df2) if change_index_to_date else suspend_df2)
    
    def load_indestry(self,industry_df,change_index_to_date=True,mapping=False,**kwarg):
        
        if mapping:
            stacked=industry_df.stack()
            lst=stacked.unique()
            mapping=pd.Series(range(len(lst)),index=lst)
            industry_df=pd.Series(mapping.reindex(stacked).values,index=stacked.index).unstack()
            
        assert industry_df.apply(is_numeric_dtype).all(), 'Industry DataFrame contains Non-numeric type'
        self._industry = (change_index(industry_df) if change_index_to_date else industry_df)
    
    def load_indexWeight(self,index_weight_df,change_index_to_date=True):
        
        assert index_weight_df.apply(is_numeric_dtype).all(), 'Index Weight DataFrame contains Non-numeric type'
        self._index_weight = (change_index(index_weight_df) if change_index_to_date else index_weight_df)

    def compile_data(self):
        '''
        This process would align tickers and time for all data.
        '''
        CI=ci_transformer()
        #columns
        CI.fit_columns(self._industry,self._suspend,self._price,self.Factor.stack(dropna=False,level=0))
        self._industry,self._suspend,self._price,factors =  CI.transform_columns(self._industry,self._suspend,self._price,self.Factor.stack(dropna=False,level=0))
        
        if self._freq=='d':
            # daily
            CI.fit_index(self._industry,self._suspend,self._price,self._index_weight)
            # transform
            self._industry,self._suspend,self._price,self._index_weight,factors2 = CI.transform_index(self._industry,self._suspend,self._price,self._index_weight,factors.unstack())
            self._industry_weight=pd.concat([self._index_weight,self._industry],axis=1,keys=['weight','ind']).stack(dropna=False).fillna(0).groupby(['dt','ind']).aggregate(sum)['weight'].unstack()
            
            self._factorDF=factors2.shift(self._day_lag)\
                                    .swaplevel(axis=1)\
                                    .sort_index(axis=1)
            # clean
            factors=factors2=None
            
        elif self._freq=='m':
            # monthly
            # Monthly factor should be have only one index each month
            
            CI.fit_index(self._industry,self._suspend,self._price,self._index_weight)
            trading_calendar=CI.index
            factors2=factors.unstack().shift(self._period_lag)
            lst = [int(i.strftime('%Y%m%d')[:6]) for i in factors2.index] # original index
            
            assert len(set(lst)) == len(lst), 'Monthly factor have a invalid frequency'
                       
            if self._fixed_date is None:
                # no fixed date
                
                # change index                           
                new_index=pd.DataFrame([[i,int(i.strftime('%Y%m%d')[:6])] for i in trading_calendar],columns=['dt','ym'])\
                                .groupby('ym').agg({'dt':max})['dt']\
                                .reindex(lst).values
                factors3=factors2.assign(dt=new_index)\
                        .loc[~pd.Series(new_index).isna().values]\
                        .set_index('dt')

            else:
                # fixed date
                target_lst=[check_time(monthmove(l)+str(self._fixed_date).zfill(2)) for l in lst]
                new_index=[pd.Series(trading_calendar).loc[pd.Series(trading_calendar).le(l)].max() for l in target_lst]
                factors3=factors2.assign(dt=new_index)\
                        .loc[~pd.Series(new_index).eq(pd.Series(new_index).shift()).values]\
                        .set_index('dt')

            # transform
            self._industry,self._suspend,self._price,self._index_weight,factors4 = CI.transform_index(self._industry,self._suspend,self._price,self._index_weight,factors3)
            self._industry_weight=pd.concat([self._index_weight,self._industry],axis=1,keys=['weight','ind']).stack(dropna=False).fillna(0).groupby(['dt','ind']).aggregate(sum)['weight'].unstack()
            self._factorDF=factors4.shift(self._day_lag)\
                                    .swaplevel(axis=1)\
                                    .sort_index(axis=1)

            # clean
            factors=factors2=factors3=factors4=None

    def clean_factor(self):
        self._factorDF=None
        self._Factors={}

    def save(self,path):
        with open(path,'wb') as f:
            f.write(pickle.dumps(self.__dict__))

    def load(self,path):
        with open(path,'rb') as f:
            dataPickle = f.read()
        self.__dict__=pickle.loads(dataPickle)

