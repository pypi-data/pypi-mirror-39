import pandas as pd

# updates files used in testing that are not part of cobrapy.
# rerun this if any changes are made to the files generated here.

biolog_base_composition = pd.read_csv('../data/biolog_base_composition.csv',sep=',')
biolog_base_dict = dict(zip(biolog_base_composition['ID'],\
                          [1000 for i in range(0,len(biolog_base_composition['ID']))]))
biolog_thresholded = pd.read_csv('../data/plata_thresholded.csv',sep='\t',index_col=0)
