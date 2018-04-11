# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:56:31 2018

@author: thePr

"""
import requests
import os

def getPics(keyWord, pages):
    params=[]
    for i in range(30,30+pages+30,30):
        params.append({
                'tn': 'resultjson_com',
                'ipn': 'rj',
                'ct': 201326592,
                'is':'',
                'fp': 'result',
                'queryWord': keyWord,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': '',
                'z': '',
                'ic': '',
                'word': keyWord,
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': '',
                'istype': '',
                'qc': '',
                'nc': 1,
                'fr': '',
                'pn': i,
                'rn': 30,
                'gsm': '5a',
                '1523433360329':'' 
                })
    url = 'https://image.baidu.com/search/index'
    urls = []
    for i in params:
        urls.append(requests.get(url,params=i).json().get('data'))
    return urls

def getImg(dataList, localPath):
    
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    
    x = 1
    for list in dataList:
        for i in list:
            if i.get('thumbURL') != None:
                print('downLoading: ', i.get('thumbURL'))
                ir = requests.get(i.get('thumbURL'))
                fileName = localPath+'/%d.jpg'%x
                pic = open(fileName, 'wb')
                pic.write(ir.content)
                pic.close()
                x += 1
            else:
                print("图片链接不存在")

#if __name__ -- '__main__':
inp = input('请输入关键词： ')
name = inp

while(True):
    inp = input('请输入下载页数，实际图片数目为30*下载页数:')
    num = int(inp)
    try:
        num = int(inp)
        break
    except:
        print('请输入正整数： ')

dataList = getPics(name, num)
getImg(dataList, str(name+'image'))