import pandas as pd
import numpy as np
import os, sys

def main():
    DATADIR = 'data'
    QADATAPATH = os.path.join(DATADIR,'qa.csv')

    qadf = pd.read_csv(QADATAPATH, sep=';')
    print(qadf.tail())

if __name__=="__main__":
    main()