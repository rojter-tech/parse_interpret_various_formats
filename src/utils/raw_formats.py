import pandas as pd
import re
from utils.errors import Error, rOjterError

def format_one(raw_text):
    """QA separation
    """
    questions = re.findall(r'(?<=Q: ).*?(?=A:)|(?<=Q: ).*?(?=\n)', raw_text)
    if len(questions) == 0:
        raise rOjterError("No way, you dont want to go there ...")
    answers =   re.findall(r'(?<=A: ).*?(?=Q:)|(?<=A: ).*?(?=\n)', raw_text)
    if (len(questions) == len(answers))and questions != []:
        Q = pd.DataFrame(questions, columns=['Q'])
        A = pd.Series(answers, name='A')
        qadf = Q.join(A)
    else:
        print('Number of questions do\'nt match up with the number of answers')
        raise rOjterError("No way, you dont want to go there ...")

    # Clean beginning and trailing whitepaces
    qalist = []
    for Q, A in zip(qadf.iloc[:,0],qadf.iloc[:,1]):
        qalist.append([Q.strip(),A.strip()])

    qadf = pd.DataFrame(qalist, columns=["Q","A"])
    print("QA tag separation suceeded.")
    return qadf

def format_two(raw_text):
    """Two line QA combination.
    """
    def process_combinations(combinations):
        qalist = []

        for combo in combinations:
            Q = combo[0].strip()
            A = combo[1].strip()
            qalist.append([Q,A])
        
        return qalist
    
    combinations = re.findall(r'(\S.*?\n)(\S.*?\n)\r\n', raw_text)
    if combinations:
        if type(combinations[0]) == tuple:
            qalist = process_combinations(combinations)
            qadf = pd.DataFrame(qalist, columns=["Q","A"])
            print("QA two line separation suceeded.")
            return qadf
        else:
            print("There is no two line combination in this file")
            raise rOjterError("No way, you dont want to go there ...")
    else:
        raise rOjterError("No way, you dont want to go there ...")

def format_ten(raw_text):
    """Raw string parser for QA pairing on same line with mixed separators.
       This format assumes that every QA pair is one the same line and that
       questions preceeds answers.
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
        print("QA general text separation suceeded.")
        return qadf
    else:
        print('Dump list contains rows that dont match')
        raise rOjterError


format_functions = [format_one, format_two, format_ten]


def try_separate_by_rawtext(wordobject, format_functions):
    check = False
    for format_function in format_functions:
        try:
            qadf = format_function(wordobject.raw_text)
            if len(qadf) != 0:
                check = True
            else:
                print("DataFrame size invalid")
                raise rOjterError
            break
        except rOjterError:
            print(wordobject.filename, "format excluded.")
    
    if check:
        return qadf
    else:
        print("")
        print("***********************************************")
        print("**!!!!Format detection did not sucess!!!!**")
        print("***********************************************")
        print("")
        print("QA by " + wordobject.filename + " format could not be determined ...")
        return wordobject.filename

