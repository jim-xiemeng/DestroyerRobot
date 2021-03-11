#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 15:18
# @Author  : vivid
# @Email   : 331597811@163.com
# @File    : s1.py
#C:\Users\vivid\PycharmProjects\untitled\requests_test\test01
import requests
from bs4 import  BeautifulSoup
import  uuid
response = requests.get(
    url='https://www.autohome.com.cn/news/',
)
response.encoding = response.apparent_encoding #解决乱码问题
#print(response.text)

soup = BeautifulSoup(response.text,features='html.parser') #features = lxml 性能强于html.parser
target = soup.find(id="auto-channel-lazyload-article") #根据属性找
#obj_li = target.find('li')#根据标签找  find找到一个  find_all找到所有
li_list = target.find_all('li')

for li in li_list:
    a=li.find('a')
    #print(a.attrs) #找到属性
    if a :
        #print("http:"+a.attrs.get('href'))
        txt = a.find('h3') #对象
        txt = a.find('h3').text
        #print(txt)

        img_url = 'http:'+a.find('img').attrs.get('src')
        #print(img_url)
        img_response = requests.get(url=img_url)
        filename = str(uuid.uuid4())+'.jpg'
        with open(filename,'wb') as f:
            f.write(img_response.content)

#https://tcms.lifeat.cn:45788/cms
