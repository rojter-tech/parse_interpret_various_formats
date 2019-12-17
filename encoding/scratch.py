import os

svenska = 'Hej hå, åäö'

data = svenska.encode('utf_8')
print(data)
print(data.decode('utf_8'))