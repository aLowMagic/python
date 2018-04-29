# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 09:15:43 2018
豆瓣电影爬虫
@author: thePr
"""

import pymysql
import requests
import numpy as np
import json
import time
import re
from bs4 import BeautifulSoup


header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

def getMovieType_Syn(url):
    try:
        r = requests.get(url='url', headers=header)
        reg = re.compile('genre">.*?</span>')
        res = reg.findall(r.text)
        Type = []
        if res != '':
            for i in res:
                Type.append(i[7:-7])
            Type = ','.join(Type)
        else:
            Type = ''
        
        soup = BeautifulSoup(r.text,"html.parser")
        text = soup.find('div', id='link-report').span.get_text()
        text = re.sub(' ','',text)
        text = re.sub('\u3000', ' ',text)
        Syn = ''
        for s in text.splitlines():
            s = s.rstrip()
            Syn += s
        
        return [Type, Syn]
    except:
        return ['','']
  
def getPic(urll):
    try:
        pic = requests.get(url=urll, headers=header)
        pic = pic.content
        return pic
    except:
        return ''

def updateDatabase(movieItems):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='visitor', password='visitor', db='movies', charset='utf8')
        cour = conn.cursor()
        if cour.execute("select %s from movies" %(movieItems['title']))==0:
            pic = getPic(movieItems['cover'])
            Type_Syn = getMovieType_Syn(movieItems['url'])
            movieType = Type_Syn[0]
            movieSyn = Type_Syn[1]
            print("电影名："+movieItems['title']+',', end=' ')
            cour.execute("insert in movies(name, coverPic, score, dirctor, actor, type, synopsis) values(%s,%s,%s,%s,%s,%s,%s,%s)" \
                         %(movieItems['title'],pic,movieItems['rate'],movieItems['directors'],movieItems['casts'],movieType,movieSyn))
    except:
        print("something wrong~")

            
          
        
    
if __name__ == '__main__':       
    for rang in np.arange(9.0,10.0,0.1):
        for start in range(0,10000,20):
            urll = "https://movie.douban.com/j/new_search_subjects?sort=S&range=%s,%s&tags=&start=%s"%(('{:.1f}'.format(rang)),('{:.1f}'.format(rang+0.1)),start)
            searchResult = requests.get(url=urll, headers=header)
            searchResult = searchResult.text
            searchResult = json.loads(searchResult)
            searchResult = searchResult["data"]
            if len(searchResult)!=0:
                for i in range(len(searchResult)):
                    items = searchResult[i]
                    updateDatabase(items)
                    time.sleep(0.5)  