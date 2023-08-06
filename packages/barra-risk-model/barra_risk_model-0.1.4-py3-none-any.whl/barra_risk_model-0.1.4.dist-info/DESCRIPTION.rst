Barra Risk Model for China A market
===================================

This is a self-build project for studying purpose only. Any commercial
usage of this project is banned.

Dependencies
------------

-  python 3.5
-  pandas 0.23.0
-  spyder 3.2.8

Sample
------

Download descriptors from Wind API and make factors

.. code:: bash

   path='your_source_file'

               #########################
               ## step1   wind update ##
               #########################
   from barra_risk_model.Wind_update.get_wind import update_wind
   dt_range_dict={
   #         'dt':(None,20181231)
           'rf':(None,20181019)
           ,'totalA':(None,20181019)
           ,'descriptor_annually':None 
           ,'index':(None,20181019)
           ,'descriptor_daily':(20181011,20181019)
           ,'descriptor_seasonal':20180930
           }

   update_wind(path,dt_range_dict)


                   #####################
                   ## step1.5  growth ##
                   #####################

   # only at the beginning of each year when new growth is downloaded
   from barra_risk_model.Factor_manufacture.make_growth import make_growth

   # example for update growth_r of 20111231
   year_range=(2011,2012)
   make_growth(year_range,path)


                   ########################
                   ## step2  integration ##
                   ########################
   from barra_risk_model.Factor_manufacture.descriptor_integration import descriptor_integration

   dt_range=(20181008,20181019)
   warm_start_quarterly=20170930 # warm start should be 1 seasons before for annual reporting and 1 seasons before for quaterly reporting
   warm_start_yearly=20161231 # 2 years before
   descriptor_integration(path,dt_range,warm_start_quarterly,warm_start_yearly)


                       ########################
                       ## step3 make factors ##
                       ########################
   from barra_risk_model.Factor_manufacture.make_factor import manufacture

   dt_range_dict={
   #        'exr':(20181008,20181019) #should cover one more day before to create return from price
   #        ,'srcap':(20181008,20181019)
   #        ,'ind':(20181008,20181019)
           'styl':(20120101,20181019)
           }
   history_start_date=20120101 #525 before styl starting date
   manufacture(path,dt_range_dict,history_start_date,mapping=True,ind_mapping_exists=True)

Make prediction of index volatility

.. code:: bash

                       #########################
                       ## step4 factor return ##
                       #########################
   from barra_risk_model.Factor_return.Factor_return_core import factor_return_manufacture

   ## start
   #dt_range=(20120101,20181019)
   #factor_return_manufacture(path,dt_range,pool='ZZ800',filter_stock_flag=True,filter_dt_flag=True)

   # renewal (use more days to keep more stocks,suggest)
   dt_range=(20180901,20181019)
   factor_return_manufacture(path,dt_range,pool='ZZ800',filter_stock_flag=True,filter_dt_flag=False)


                   #######################################
                   ## step5 factor cov and specfic risk ##
                   #######################################
   import numpy as np
   from RNWS import read,write
   from barra_risk_model.Factor_matrix_core import cov_matrix_gen_range
   from barra_risk_model.Specific_matrix_core import spc_matrix_gen_range


   start=20140312
   end=20181019

   Fct_return= read.read_df(path+'/factor_return_data',file_pattern='Fct_return',start=start,end=end)
   F_all= cov_matrix_gen_range(Fct_return)

   Spc_return=read.read_df(path+'/factor_return_data',file_pattern='Spc_return',start=start,end=end)
   SRCap=read.read_df(path+'/srcap','srcap',start=start,end=end)
   stock_pool=read.read_srs(path+'/index/ZZ800','Stk_ZZ800',start=start,end=end)
   X_all= read.read_dict(path+'/factor_return_data',file_pattern='X1',start=start,end=end)
   S_all=spc_matrix_gen_range(Spc_return=Spc_return,X_all=X_all,stock_pool=stock_pool,cap=np.square(SRCap))

   renewal_dt=20140312
   F_all_tmp={dt:F_all[dt] for dt in read.reading_data.trading_dt[(read.reading_data.trading_dt>=renewal_dt)&(read.reading_data.trading_dt<=end)]}
   S_all_tmp=S_all.loc[renewal_dt:]

   write.write_dict(F_all_tmp,path=path+'/factor_cov_matrix',file_pattern='factor_cov')
   write.write_df(S_all_tmp,path=path+'/specific_volatility',file_pattern='specofoc_vol')

                           #############################
                           # step6 one day prediction ##
                           #############################
   import numpy as np
   from RNWS import read,write
   from barra_risk_model.Factor_matrix_core import cov_matrix_oneday
   from barra_risk_model.Specific_matrix_core import spc_matrix_oneday

   start=20170508
   end=20180508

   Fct_return= read.read_df(path+'/factor_return_data',file_pattern='Fct_return',start=start,end=end)
   F_one=cov_matrix_oneday(Fct_return,dt=20180508)

   Spc_return=read.read_df(path+'/factor_return_data',file_pattern='Spc_return',start=start,end=end)
   X_all= read.read_dict(path+'/factor_return_data',file_pattern='X1',start=start,end=end)
   stock_pool=read.read_srs(path+'/index/ZZ800','Stk_ZZ800',start=start,end=end)
   SRCap=read.read_df(path+'/srcap','srcap',start=start,end=end)
   S_one=spc_matrix_oneday(Spc_return=Spc_return,dt=20180508,X_all=X_all,stock_pool=stock_pool,cap=np.square(SRCap))
   # S_one predict one day specific volatility, requiring 128 days to preoduce.

                           ###############################
                           ## step7 evaluate prediction ##
                           ###############################
   from barra_risk_model.Bias_stats import bs_F,bs,bs_window,bs_f_window,real_std,predicted_std

   import datetime
   import matplotlib.pyplot as plt


   start=20140312
   end=20181019

   F_all= read.read_dict(path+'/factor_cov_matrix',file_pattern='factor_cov',start=start,end=end)
   R_all= read.read_df(path+'/factor_return_data',file_pattern='R',start=start,end=end)
   X_all= read.read_dict(path+'/factor_return_data',file_pattern='X1',start=start,end=end)
   S_all= read.read_df(path+'/specific_volatility',file_pattern='specofoc_vol',start=start,end=end)
   W= read.read_df(path+'/index/HS300',file_pattern='Stk_HS300',start=start,end=end,dat_col=3,inx_col=1)
   W=W.replace('None',np.nan).astype(float)
   W2=W.fillna(0)
   #W2=W2.where(W2==0)

   def plot_bs(R_all,F_all,X_all,S_all,W):
       bs_f=bs_F(R_all,F_all,X_all,W) 
       bs_fw=bs_f_window(R_all,F_all,X_all,W)
       bs_=bs(R_all,F_all,X_all,S_all,W) 
       bs_w=bs_window(R_all,F_all,X_all,S_all,W)

       bs_fw.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in bs_fw.index]
       bs_w.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in bs_w.index]

       plt.figure(figsize=(10,6))
       plt.plot(bs_w,label='bs')
       plt.plot(bs_fw,label='bs_f')
       plt.gcf().autofmt_xdate()
       plt.legend()
       plt.show()
       print(bs_f,bs_)

   def plot_vol(R_all,F_all,X_all,S_all,W):
       rv=real_std(R_all,W)
       pv=predicted_std(F_all,S_all,X_all,W)

       rv.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in rv.index]
       pv.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in pv.index]

       plt.figure(figsize=(10,6))
       plt.plot(rv,label='real volatility')
       plt.plot(pv,label='predicted volatility')
       plt.gcf().autofmt_xdate()
       plt.legend()
       plt.show()

   plot_vol(R_all,F_all,X_all,S_all,W2)

   rv=real_std(R_all,W2)
   pv=predicted_std(F_all,S_all,X_all,W2)
   pv2=pv.reset_index()
   rv2=rv.reset_index()
   pv3=pv.iloc[np.where((pv2['index']//100).pct_change()!=0)]
   rv3=rv.iloc[np.where((rv2['index']//100).pct_change()!=0)]
   rv3.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in rv3.index]
   pv3.index=[datetime.datetime.strptime(str(i),'%Y%m%d') for i in pv3.index]
   plt.figure(figsize=(10,6))
   plt.plot(rv3,label='real volatility')
   plt.plot(pv3,label='predicted volatility')
   plt.gcf().autofmt_xdate()
   plt.legend()
   plt.show()


