"""Reading standardized csv, xlsx, gzip pickle and json files"""

import pandas as pd
import os, json

DATADIR = os.path.join(os.pardir,'data')
CSVFILE = 'qa.csv';     CSVFILEPATH = os.path.join(DATADIR,CSVFILE)
EXCELFILE = 'qa.xlsx';  EXCELFILEPATH = os.path.join(DATADIR,EXCELFILE)
PICKLEFILE = 'qa.gzip'; PICKLEFILEPATH = os.path.join(DATADIR,PICKLEFILE)
JSONFILE = 'qa.json';   JSONFILEPATH = os.path.join(DATADIR,JSONFILE)

def load_json_data(jsonfilepath):
    with open(jsonfilepath, mode='rt', encoding='utf_8') as f:
        json_dict = json.loads(f.read())
    Q = pd.DataFrame(list(json_dict.keys()), columns=['Q'])
    A = pd.Series(list(json_dict.values()), name='A')
    qadf = pd.DataFrame(Q.join(A))
    return qadf

def main():
    sheet_names = pd.ExcelFile(os.path.join(DATADIR,'qa.xlsx')).sheet_names
    print("Excel sheet names", sheet_names)

    qadf_csv = pd.read_csv(CSVFILEPATH, sep=';')
    qadf_xlsx = pd.read_excel(EXCELFILEPATH, sheet_name=sheet_names[0])
    qadf_gzip = pd.read_pickle(PICKLEFILEPATH, compression='gzip')
    qadf_json = load_json_data(JSONFILEPATH)

    print("CSV Output"); print(qadf_csv.tail(), end='\n\n')
    print("Excel Output"); print(qadf_xlsx.tail(), end='\n\n')
    print("Pickle Output"); print(qadf_gzip.tail(), end='\n\n')
    print("JSON Output"); print(qadf_json.tail(), end='\n\n')

if __name__=="__main__":
    main()