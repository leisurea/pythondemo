import requests
import re
from urllib.parse import urlencode
from download_list import getVideoUrl
from util.UAPool import data as UAPool_List
import random

def search(keyword):
    url = 'http://www.01kuku.com/search.asp'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'If-Modified-Since': 'Sun, 29 Sep 2019 10:21:06 GMT',
        'If-None-Match': 'W/"0d5749aaf76d51:0"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.68tmm.com:8888',
        'Referer': 'http://www.68tmm.com:8888/diao/se28',
        'User-Agent': random.choice(UAPool_List)
    }
    requestdata = 'type=vedio&searchword=%s'%keyword
    # respone = requests.post(url,params=urlencode(data),headers=header)
    
    try:
        respone = requests.post(url,data=requestdata.encode('gb2312'),headers=header)
    except Exception as ex:
        print('===========搜索失败异常：%s================='%ex)
        print('===========重启搜索=================')
        search(keyword)
        return

    if respone.status_code != 200:
        print('搜索失败：%i' %respone.status_code)
        return
    respone.encoding = 'gb2312'

    videobox = re.findall(r'<div class="video_box"> (.*?)</div>',respone.text,re.S)
    # print(videobox)
    for video in videobox:
        # print(video)
        list_video = re.findall(r'<a href="(.*?)"  target="_blank"><img src="(.*?)" title="(.*?)"',video,re.S)
        # print(list_video[0])
        video_url,img_url,title = list_video[0]
        # getVideoUrl(video_url,title)
        saveVideoInfo(keyword, list_video[0])

    searchNext(2,keyword)

#搜索的第二页变成get了，interesting
def searchNext(page,keyword):

    params = {
        'page':page,
        'searchword':keyword,
        'searchtype':-1
    }
    baseUrl = 'http://www.01kuku.com/search.asp?'
    url = baseUrl + urlencode(params,encoding='gb2312')
    # url = 'http://www.01kuku.com/search.asp?page=%i&searchword=%s&searchtype=-1'%(page, keyword.encode('gb2312'))
    print('================搜索到了第%i页 url:%s'%(page, url))
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'If-Modified-Since': 'Sun, 29 Sep 2019 10:21:06 GMT',
        'If-None-Match': 'W/"0d5749aaf76d51:0"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.68tmm.com:8888',
        'Referer': 'http://www.01kuku.com/search.asp',
        'Cookie':'ASPSESSIONIDCACRCSRQ=BAMIFHEAHEEKMCAIFNEDDDBM; UM_distinctid=16d8116a74ea0a-09d7d071a7ba8f-1d3b6b55-1fa400-16d8116a74f486; CNZZDATA1277478266=1484435840-1569827673-null%7C1569827673; Hm_lvt_9cf0b303e583fa99d34ffe27b2096780=1569828809; Hm_lpvt_9cf0b303e583fa99d34ffe27b2096780=1569828809',
        'User-Agent': random.choice(UAPool_List)
    }
    try:
        respone = requests.get(url, headers=header)
    except Exception as ex:
        print('===========next搜索失败异常：%s================='%ex)
        print('===========next重启搜索=================')
        searchNext(page,keyword)
        return

    if respone.status_code != 200:
        print('next搜索失败：%i' %respone.status_code)
        return
    respone.encoding = 'gb2312'
    videobox = re.findall(r'<div class="video_box"> (.*?)</div>',respone.text,re.S)
    # print(videobox)
    for videoitem in videobox:
        # print(video)
        video = re.findall(r'<a href="(.*?)"  target="_blank"><img src="(.*?)" title="(.*?)"',videoitem,re.S)
        print(video[0])
        video_url,img_url,title = video[0]
        # getVideoUrl(video_url,title)
        saveVideoInfo(keyword, video[0])

    #获取总页数
    pagination = re.findall(r'<div class="pagination">(.*?)</div>',respone.text,re.S)
    list_page = re.findall('page=(.*?)&searchword',pagination[0],re.S)
    if page < int(max(list_page)):
      searchNext(page+1, keyword)

#保存视频信息到本地
def saveVideoInfo(keyword,source):
    video_url, img_url, title = source
    with open('/Users/leisure/Downloads/python_data/video/%s/%s.txt' %(keyword,keyword), 'a') as f:
        f.write(video_url+'@@@'+title)
        f.write('\n')
        print('保存成功:%s' %str(source))


#保存视频信息到本地
def getVideoInfo(keyword):
    # source = video_url, img_url, title
    xianger = []
    with open('/Users/leisure/Downloads/python_data/video/%s/%s.txt' %(keyword,keyword), 'r') as f:
        # source = f.readline()
        # print('保存成功:%s' %source)
        for line in f:
            xianger.append(line.replace('\n',''))

    return xianger

if __name__ == '__main__':
    # search('萝莉')
    searchNext(2,'萝莉')



