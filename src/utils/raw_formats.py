import pandas as pd
import re
from utils.wapi import Error, rOjterError

def format_one(raw_text):
    """Raw string parser for QA pairing on same line with mixed separators.
       This format assumes that every QA pair is one the same line and that
       questions preceeds answers.
    
    Arguments:
        raw_text {str} -- [description]
    
    Raises:
        rOjterError: [description]
    
    Returns:
        [type] -- [description]
    """

    splitqa, dump = [], []
    for line in re.findall(r"\S.*\n", raw_text):
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
        raise rOjterError
