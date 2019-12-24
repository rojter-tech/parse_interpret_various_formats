import pandas as pd
import re

class Error(Exception):
   """Base class for other exceptions"""
   pass

class rOjterError(Error):
   """Raised when rOjter is just too smart not to handle this"""
   pass

def format_one(raw_text):
    splitqa, dump = [], []
    for line in raw_text.split('\n'):
        if not line[-1:] == '.' and len(line) == 2:
            line+='.' # Add missing last punctuation
        regsplit = re.findall(r".*\?|\S.*?\.|\S.*?\n|\ .*?\n", line) # Split by pattern
        if len(regsplit) == 2:
            regsplit[0] = regsplit[0].strip()
            regsplit[1] = regsplit[1].strip()
            splitqa.append(regsplit)
        else:
            dump.append(line)
            print("Dump!")
            raise rOjterError("No way, you dont want to go there ...")

    if len(dump) == 0:
        print('Hurray No lines in dump list.')
        qadf = pd.DataFrame(splitqa, columns=['Q','A'])
        return qadf
    else:
        print('Dump list contains rows that dont match')
        assert 1 == 0
