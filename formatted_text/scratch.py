import pandas as pd
import numpy as np
import os, re

# Generated data
DATADIR = os.path.join(os.pardir,'data')
FORMATTED_DATADIR = "formatted_text_data"
GENERATED_TEXTFILE1 = "format1.txt"
TEXTFILE1_PATH = os.path.join(DATADIR,FORMATTED_DATADIR,GENERATED_TEXTFILE1)

with open(TEXTFILE1_PATH, mode='rt', encoding='utf_8') as f:
    utf8_filestring = f.read()

# Find all questions and answers, assuming they are in order
questions = re.findall(r'(?<=Q: ).*?(?=A:)|(?<=Q: ).*?(?=\n)', utf8_filestring)
answers =   re.findall(r'(?<=A: ).*?(?=Q:)|(?<=A: ).*?(?=\n)', utf8_filestring)

if len(questions) == len(answers):
    Q = pd.DataFrame(questions, columns=['Q'])
    A = pd.Series(answers, name='A')
    qadf = Q.join(A)
else:
    print('Number of questions dont match up with the number of answers')

# Clean beginning and trailing whitepaces
qalist = []
for Q, A in zip(qadf.iloc[:,0],qadf.iloc[:,1]):
    while re.match(r'\s', Q[0]):
        Q=Q[1:]
    while re.match(r'\s', Q[-1]):
        Q=Q[:-1]

    while re.match(r'\s', A[0]):
        A=A[1:]
    while re.match(r'\s', A[-1]):
        A=A[:-1]
    qalist.append([Q,A])

qadf = pd.DataFrame(qalist, columns=[Q,A])
print(qadf)