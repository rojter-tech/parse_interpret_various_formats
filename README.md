# Parsing Microsoft xml based formats with parse_interpret_various_formats
Version: 0.0.1
Development kit

Primary feature : Parse, read and separate questions and answers from QA documents in Microsofts Word `docx`- and `xlsx` format.

Tools including `xml.etree.ElementTree` to effectivley parse internal xml files that is the fundamental markup language of many of Microsoft's format.

## Installation of parse_interpret_various_formats

### For **macOS/UNIX**

With [`python3`](https://www.python.org/downloads/release/python-381/) and [`pip`](https://pypi.org/project/pip/):

Bash

```bash
git clone https://github.com/rojter-tech/parse_interpret_various_formats.git ~/parse_interpret_various_formats
```

Create a new environment inside the repo and source it
```bash
python -m venv ~/parse_interpret_various_formats
source ~/parse_interpret_various_formats/bin/activate
python -m pip install -U pip
```

Install dependencies
```bash
cd ~/parse_interpret_various_formats
pip install -r requirements/dev.txt
python setup.py bdist_wheel
pip install -e .
```

### For Windows


With [`python3`](https://www.python.org/downloads/release/python-381/) and [`pip`](https://pypi.org/project/pip/):

Powershell

```bash
git clone https://github.com/rojter-tech/parse_interpret_various_formats.git $HOME\parse_interpret_various_formats
```

Create a new environment inside the repo and source it
```bash
python -m venv $HOME\parse_interpret_various_formats
$HOME\parse_interpret_various_formats\Scripts\activate
$HOME\parse_interpret_various_formats\Scripts\activate.bat
python -m pip install -U pip
```

Install dependencies
```bash
cd $HOME\parse_interpret_various_formats
pip install -r .\requirements\dev.txt
python setup.py bdist_wheel
pip install -e .
```
