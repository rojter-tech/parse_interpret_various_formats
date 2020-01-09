import os
from utils.format_detection_tools import load_word_objects
from utils.format_detection_tools import multiple_object_diagnostics

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
# Source files
wordobjects = load_word_objects(WORDDATADIR)

def main():
    wordobjects = load_word_objects(WORDDATADIR)
    multiple_object_diagnostics(wordobjects)


if __name__ == "__main__":
    main()
