import pandas as pd
import numpy as np
import os

# Source data
DATADIR = os.path.join(os.pardir,'data')
CSVFILE = 'qa.csv'; CSVFILEPATH = os.path.join(DATADIR,CSVFILE)

# Generated data
FORMATTED_DATADIR = "formatted_text_data"
GENERATED_TEXTFILE1 = "format1.txt"
TEXTFILE1_PATH = os.path.join(DATADIR,FORMATTED_DATADIR,GENERATED_TEXTFILE1)

def random_insert(Q, A):
    CRLF = '\r\n'
    insert_string = "Q: " + Q + ' ' + "A: " + A + CRLF
    rev_insert_string = "A: " + A + ' ' + "Q: " + Q + CRLF
    random_integer = np.random.randint(6)
    random_linefeed = np.random.randint((10,10,10)) + 1
    if random_integer == 0:
        insert_string = insert_string
    if random_integer == 1:
        insert_string = rev_insert_string
    if random_integer == 2:
        insert_string = insert_string + random_linefeed[0]*CRLF
    if random_integer == 3:
        insert_string = rev_insert_string + random_linefeed[0]*CRLF
    if random_integer == 4:
        insert_string = random_linefeed[0]*CRLF + "A: " + A + \
                        random_linefeed[1]*CRLF + \
                        "Q: " + Q + random_linefeed[2]*CRLF
    if random_integer == 5:
        insert_string = random_linefeed[0]*CRLF + "Q: " + Q + \
                        random_linefeed[1]*CRLF + \
                        "A: " + A + random_linefeed[2]*CRLF
    return insert_string

def main():
    f = open(TEXTFILE1_PATH,mode="wt",encoding='utf_8')
    f.close
    qadf_csv = pd.read_csv(CSVFILEPATH, sep=';')
    with open(TEXTFILE1_PATH, mode='at', encoding='utf_8') as f:
        for Q, A in zip(qadf_csv.iloc[:,0], qadf_csv.iloc[:,1]):
            insert_string = random_insert(Q, A)
            f.write(insert_string)

if __name__=="__main__":
    main()