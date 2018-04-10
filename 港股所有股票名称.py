# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 18:03:43 2018

@author: thePr
"""

import re
import requests

url = 'http://quote.eastmoney.com/hk/HStock_list.html'
tx = ''
try:
    r = requests.get(url, timeout = 30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    tx = r.text
except:
    print('wrong0')
searchMod = r'(target="_blank">)(\([\d]{5}\).+)(</a>)'
r = re.findall(searchMod, tx)
res = []
for i in range(len(r)):
    mid = r[i]
    res.append(mid[1])
print(res)