
Agmodeling
===========
Statistical modeling tools, to unify model creation and scoring based on python

package agmodeling.setscoring implements a part of the SET method for comparing
sensor output as described by :

An Evaluation Tool Kit of Air Quality 1 Micro-Sensing Units 
(Barak Fishbain1,Uri Lerner, Nuria Castell-Balaguer)



What's New
===========
- (2018/11) First version (v 0.3)



Dependencies
=============

Agmodeling is written to be use with python 2.7
It requires Pandas, numpy and  scipy
It requires `Pandas`::

    pip install pandas
    pip install numpy
    pip install scipy
    
    
Installations
=============

    pip install agmodeling
    

Uses cases
========== 

	from agmodeling.scoring.set_method import get_IPI_score
	import pandas as pd
	
	file = u'sample_data.xlsx'
	print (u'Read excel data file : %s'%file)
	df = pd.read_excel(file)
    ipi = get_IPI_score(df[u'PM10_REF'], df[u'PM10_MOD_EARTH'])
    print ipi
    
     Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.763240  : 0.061937  : 0.909195  : 0.657553  : 0.832455  : 0.990418   :: 0.848801
	
	0.848801
	
	
You can run the whole demo inside the package   

	cd demo
	python .\demo_SET_scoring.py
	Read excel data file : sample_data.xlsx
	containing 2568 data
	
	Score IPI for PM25_RAW
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.492835  : 0.238941  : 0.639916  : 0.417968  : 0.575632  : 0.980072   :: 0.648981
	
	Score IPI for PM25_MOD_QUAD
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.687539  : 0.102816  : 0.747821  : 0.524258  : 0.695786  : 0.980072   :: 0.756295
	
	Score IPI for PM25_MOD_EARTH
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.648910  : 0.092760  : 0.800773  : 0.537126  : 0.713852  : 0.980072   :: 0.765357
	
	Score IPI for PM10_RAW
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.486604  : 0.264435  : 0.454199  : 0.269705  : 0.393423  : 0.990418   :: 0.560331
	
	Score IPI for PM10_MOD_QUAD
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.742056  : 0.074365  : 0.866073  : 0.612143  : 0.789426  : 0.990418   :: 0.821408
	
	Score IPI for PM10_MOD_EARTH
	 Match     : RMSE      : Pearson   : Kendall   : Spearman  : LFE        :: IPI
	 0.763240  : 0.061937  : 0.909195  : 0.657553  : 0.832455  : 0.990418   :: 0.848801
	
	========================================
	Results :
	           RAW  MOD_QUAD  MOD_EARTH
	PM10  0.560331  0.821408   0.848801
	PM25  0.648981  0.756295   0.765357
	
	Fin du programme

