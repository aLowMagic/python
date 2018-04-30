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



header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

def getMovieType_Syn(url):
    try:
        r = requests.get(url=url, headers=header)
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
        print('proccess type change succeed')
        return [Type, Syn]
    
    except:
        print('def getMovieType_Syn was wrong')
        return ['','']
  
def getPic(urll):
    pic = requests.get(url=urll, headers=header)
    pic = pic.content
    pic = pymysql.escape_string(str(pic))
    print('proccess getPic succedd')
    return pic

def listChange(param):
    strr = ','.join(param)
    print('porccces listChange succedd')
    return strr

def updateDatabase(movieItems):
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='visitor', \
                               password='visitor', db='test0', charset='utf8')
        cour = conn.cursor()
    except:
        print('didn\'t open the database')
        
    try:
        if cour.execute("select * from movies where movie_name='%s';" %(movieItems['title']))==0:
            pic = getPic(movieItems['cover'])
            Type_Syn = getMovieType_Syn(movieItems['url'])
            movieType = Type_Syn[0]
            movieSyn = Type_Syn[1]
            cour.execute("INSERT INTO movies(movie_name, coverPic, score, director, actor, movie_type, synopsis) VALUES('%s','%s',%s,'%s','%s','%s','%s');" \
                         %(movieItems['title'],pic,movieItems['rate'], \
                           listChange(movieItems['directors']),listChange(movieItems['casts']),movieType,movieSyn))
            conn.commit()
            print("电影名："+movieItems['title']+'爬取成功'+'\n')
    except:
        print('电影'+movieItems['title']+'数据上传失败')
        
    cour.close()
    conn.close()
    return
            
    
if __name__ == '__main__':       
    countor = 0
    for rang in np.arange(10.0,9.0,-0.1):
        for start in range(0,10000,20):
            urll = "https://movie.douban.com/j/new_search_subjects?sort=S&range=%s,%s&tags=&start=%s" %('{:.1f}'.format(rang-0.1),'{:.1f}'.format(rang),start)
            searchResult = requests.get(url=urll, headers=header)
            searchResult = searchResult.text
            searchResult = json.loads(searchResult)
            searchResult = searchResult["data"]
            if len(searchResult)!=0:
                for i in range(len(searchResult)):
                    items = searchResult[i]
                    updateDatabase(items)
                    time.sleep(0.5)  
            else:
                break
    print('爬取结束，谢谢惠顾')