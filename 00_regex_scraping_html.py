import os, re
from numpy import array, savetxt
import pandas as pd
DATADIR = 'data'
HTMLFILE = 'trivial.html'
FILEPATH = os.path.join(DATADIR,HTMLFILE)

qalist = []
with open(FILEPATH) as htmlfile:
    for line in htmlfile:
        questiontag = re.findall(r'<h3.*?>.*?</h3>', line)
        if questiontag:
            question = re.findall(r'(?<=>).*(?=<span)', questiontag[0])
            answer = re.findall(r'(?<=<p>).*?(?=</p>)', line)
            if answer:
                qalist.append([str(question[0]),str(answer[0])])
            else:
                print(question[0],' : ' , 'has multiple answers!')

qadf = pd.DataFrame(qalist)
# Make sure that any semicolon is not present in the data
qadf.replace(';', ':', inplace=True, regex=True)
qadf.replace(r'Answer:.*?(?=\S)', '', inplace=True, regex=True)

SAVEPATH = os.path.join(DATADIR,'qa.csv')
savetxt(SAVEPATH, array(qadf, dtype=object), 
    header='Q;A', delimiter=';', fmt="%s", comments='')

print(pd.read_csv(SAVEPATH, sep=';').head())