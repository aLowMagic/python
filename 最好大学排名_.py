# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:47:00 2018

@author: thePr
"""

import requests
from bs4 import BeautifulSoup
import bs4

ulist = []
url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html'
try:
    r = requests.get(url,timeout = 10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
except:
    print("wrong")
soup = BeautifulSoup(r.text,"html.parser")
for tr in soup.find('tbody').children:
    if isinstance(tr, bs4.element.Tag):
        tds = tr('td')
        ulist.append([tds[0].string, tds[1].string, tds[3].string])
mod = "{0:^10}\t{1:{3}^10}\t{2:^10}"
print(mod.format("排名", "学校名称", "总分", chr(12288)))
for i in range(20):
    u = ulist[i]
    print(mod.format(u[0],u[1],u[2],chr(12288)))
    