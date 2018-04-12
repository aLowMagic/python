# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 20:12:25 2018
实现图片转化为文字的功能，使用时可以把字体变小这样像一点= =
@author: thePr
"""

from PIL import Image


def picChange(r,g,b,alpha = 256):
    if alpha == 0:
        return ''
    ascii_char = list("1234567890abcdefghijklmnopqrstuvwx z")
    gray = len(ascii_char)*(r * 0.333 + g * 0.333 + b * 0.3)/(alpha+1)
    grayValue = ascii_char[int(gray)] + ascii_char[int(gray)]
    return grayValue

if __name__ == '__main__':
    pic = Image.open('C:/Users/thePr/Documents/pythontest/timg.jpg')
    picSize = pic.size
    pic = pic.resize((int(picSize[0]/5), int(picSize[1]/5)), Image.NEAREST)
    txt = ''
    for i in range(pic.size[1]):
        for j in range(pic.size[0]):
            txt += picChange(*pic.getpixel((j, i)))
        txt += '\n'
    with open('output.txt','w') as f:
        f.write(txt)