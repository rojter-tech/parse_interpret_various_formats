"""Reading a standard csv and xlsx"""

import pandas as pd
import numpy as np
import os, sys

DATADIR = 'data'

def main():
    sheet_names = pd.ExcelFile(os.path.join(DATADIR,'qa.xlsx')).sheet_names
    print(sheet_names)

    qadf_csv = pd.read_csv(os.path.join(DATADIR,'qa.csv'), sep=';')
    qadf_xlsx = pd.read_excel(os.path.join(DATADIR,'qa.xlsx'), sheet_name=sheet_names[0])

    print(qadf_csv.tail())
    print(qadf_xlsx.tail())

if __name__=="__main__":
    main()