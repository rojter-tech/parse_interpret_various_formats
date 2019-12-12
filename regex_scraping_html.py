import sys, os, re
import numpy as np
import pandas as pd
DATADIR = 'data'
HTMLFILE = 'trivial.html'
FILEPATH = os.path.join(DATADIR,HTMLFILE)

qalist = []
with open(FILEPATH) as htmlfile:
    for line in htmlfile:
        questiontag = re.findall('<h3.*?>.*?</h3>', line)
        if questiontag:
            question = re.findall('(?<=>).*(?=<span)', questiontag[0])
            answer = re.findall('(?<=<p>).*?(?=</p>)', line)
            if answer:
                qalist.append([str(question[0]),str(answer[0])])
            else:
                print(question[0],' : ' , 'has multiple answers!')

qadf = pd.DataFrame(qalist)
# Make sure that any semicolon is not present in the data
qadf.replace(';', ':', inplace=True, regex=True)
qadf.replace('Answer:.*?(?=\S)', '', inplace=True, regex=True)

SAVEPATH = os.path.join(DATADIR,'qa.csv')
np.savetxt(SAVEPATH, np.array(qadf, dtype=object), 
    header='Q;A', delimiter=';', fmt="%s", comments='')

print(pd.read_csv(SAVEPATH, sep=';').tail())