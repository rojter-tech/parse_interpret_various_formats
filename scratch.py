import pandas as pd
import numpy as np
import os, sys

DATADIR = 'data'
QADATAPATH = os.path.join(DATADIR,'qa.csv')

qadf = pd.read_csv(QADATAPATH, sep=';')
for row in np.array(qadf):
    print('<b>'+row[0]+'</b>',row[1]+'<br>')