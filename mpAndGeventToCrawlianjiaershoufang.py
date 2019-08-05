#!/usr/bin/python3
#-*- coding: utf-8 -*-
#-*- author:zhangjiao -*-
'''
进程＋协程＋正则
主页： https://sz.lianjia.com/ershoufang
区域：一个区域对应一个进程
分区爬取：拿到页码分页爬取［协程］
将数据写到csv文件中，按区域写［标题与价格］
'''
from gevent import monkey;monkey.patch_all()#导入猴子补丁#可以实现协程的自动切换
import gevent
import urllib.request
import ssl
import threading
import os
import time
import re
import csv
import multiprocessing


def getdata(url):
    context = ssl._create_unverified_context()
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    requset = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(requset, context=context)
    data = response.read()

    return data.decode()


def getarea(url):
    data = getdata(url)
    # quyuList = re.findall(r'<a href="/ershoufang/(.*?qu)/".*?>(.*?)</a>',data,re.S)
    datalist = re.findall(r'<div data-role="ershoufang" >(.*?)</div>',data,re.S)
    # print(len(datalist))
    quyuList = re.findall(r'<a href="(.*?)".*?>(.*?)</a>',datalist[0],re.S)
    # print(quyuList)
    return dict(quyuList)

def getPageNum(url):
    data = getdata(url)
    # print(url)
    # pageList = re.findall(r'class="page-box house-lst-page-box".*?page-data=(.*?)>',data,re.S)
    pageList = re.findall(r'totalPage":(.*?),',data,re.S)
    # print(pageList)
    return int(pageList[0])

def getPageData(pageurl,areaname):
    data = getdata(pageurl)
    # dataList =re.findall(r'<li class="clear LOGCLICKDATA".*?data-is_focus="" data-sl="">(.*?)</a> .*?class="totalPrice"><span>(.*?)</span>',data,re.S)
    # dataList =re.findall(r'<li class="clear.*?class="totalPrice"',data,re.S)
    dataList =re.findall(r'<li class="clear.*?data-is_focus="" data-sl="">(.*?)</a>.*?class="totalPrice"><span>(.*?)</span>',data,re.S)
    # print(len(dataList))
    # print(dataList[0])
    with open(areaname+".csv","a",encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(dataList)




def func(areapath,areaname):
    pagenum = getPageNum(areapath)
    # print(pagenum)
    gList = []
    for i in range(1,pagenum+1):
        pagepath = areapath+"pg"+str(i)
        g = gevent.spawn(getPageData,pagepath,areaname)
        gList.append(g)
    gevent.joinall(gList)





if __name__ == '__main__':
    url = "https://sz.lianjia.com/ershoufang"
    os.mkdir("file")
    os.chdir("file")
    areadict = getarea(url)
    path ="https://sz.lianjia.com"
    print(areadict)
    for areaurl,areaname in areadict.items():
        p = multiprocessing.Process(target=func,args=(path+areaurl,areaname))
        p.start()
    pass

    # path = "https://sz.lianjia.com/ershoufang/longgangqu/pg2/"
    # getPageData(path)
