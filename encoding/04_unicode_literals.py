import os, sys

print(sys.getdefaultencoding())
print('')

def chartouni(char):
    chartodec = ord(char)
    dectohex_str = hex(chartodec).split('x')[-1]
    if len(dectohex_str) == 0:
        return "\\u0000"
    elif len(dectohex_str) == 1:
        return "\\u000" + dectohex_str
    elif len(dectohex_str) == 2:
        return "\\u00" + dectohex_str
    elif len(dectohex_str) == 3:
        return "\\u0" + dectohex_str
    else:
        return "\\u" + dectohex_str

def unitochar(uni):
    return chr(ord(uni))

svenska = r'Hej hå, åäö'
data = svenska.encode('utf_8')
print("Raw string representation (UTF 8):", svenska)
print("Bytes ASCII string and literal representation (ASCII/literal):", data)
print("Type of data:", type(data))
print("Decode back:",data.decode('utf_8'))

print(b'\x20 \x21 \x22 \x23 \x24'.decode('utf_8'))

print('Uncode code point of first accesible character in latin1:',chartouni(' '))
print('Uncode code point of last accesible character in latin1:',chartouni('ÿ'))
print('Uncode code point of bullet character:',chartouni('•'))
print('Uncode code point of Å character:',chartouni('Å'))
print('Uncode code point of å character:',chartouni('å'))

print("")
unitable = []
row = []
for i in range(2**8):
    row.append(chr(i))
    if i % 16 == 15:
        unitable.append(row)
        row = []

from pprint import pprint as pp
pp(unitable, width=150, compact=True)
#print(pd.DataFrame(unitable, dtype=object))