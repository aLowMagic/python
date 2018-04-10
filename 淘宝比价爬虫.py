# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 19:24:15 2018

@author: thePr
"""

import requests
import re

def getHtml(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getPage(pList, html):
    rModTitle = r'"raw_title":".*?"'
    rModPrice = r'"view_price":"[\d.]*"'
    try:
        titleFind = re.findall(rModTitle,html)
        priceFind = re.findall(rModPrice,html)
        print(len(titleFind))
        for i in range(len(titleFind)):
            print
            price = eval(titleFind[i].split(':')[1])
            title = eval(priceFind[i].split(':')[1])
            pList.append([price, title])
        return pList
    except:
        print("wrong getPage def")
        return ""
    
def printPage(pList):
    modPrint = "{0:4}\t{1:10}\t{2:^10}"
    print(modPrint.format("序号","商品名称","价格", chr(12288)))
    count = 0
    for i in pList:
        count += 1
        print(modPrint.format(count,str(i[0])[0:5], str(i[1]), chr(12288)))
    
if __name__ == "__main__":
    url = 'https://s.taobao.com/search?q=滑雪板'
    html = getHtml(url)
    pList = []
    pList = getPage(pList, html)
    printPage(pList)
    