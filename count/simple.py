#!/usr/bin/python3

import json
from urllib.request import urlopen

url = "https://bulletin.pseudovote.net/"
data = json.load(urlopen(url))
hääli = 200*[0]

for hääl in data["votes"]:
    kandinr = int(hääl[2])
    hääli[kandinr] = hääli[kandinr] + 1
            
for hääl in enumerate(hääli):
    if hääl[1] != 0:
         print(hääl)