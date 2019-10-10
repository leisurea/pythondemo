import requests
import re
from util.UAPool import data as UAPool_List
import random
import multiprocessing
import time

def getHomeList():

    url = 'http://www.68tmm.com:8888/diao/se28'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=16d80d57701f3-0c620ed80071c8-1d3b6b55-1fa400-16d80d577024ad; CNZZDATA1277477495=160265188-1569820341-%7C1569820341; Hm_lvt_79465e30fb78fd3df45b55fcbc3ee72b=1569824536; AD_Time_480="idx:1"; Hm_lpvt_79465e30fb78fd3df45b55fcbc3ee72b=1569892650',
        'Host': 'www.68tmm.com:8888',
        'If-Modified-Since': 'Sun, 29 Sep 2019 10:21:06 GMT',
        'If-None-Match': 'W/"0d5749aaf76d51:0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(UAPool_List)
    }
    
    respone = requests.get(url, headers=header)

    if respone.status_code != 200 :
        print('网站响应失败！！！')
        return
    respone.encoding = 'gb2312'
    list_video = re.findall(r'<div class="video_box"> <a href="(.*?)" target="_blank"><img src="(.*?)" title="(.*?)"',respone.text,re.S)
    for mix in list_video:
        video_url,img_url,title = mix
        video_url = "http://www.68tmm.com:8888"+video_url
        # print(video_url,img_url,title)
        # getVideoUrl(keyword,video_url,title)
        # break


    return ""

def getVideoUrl(keyword, video_url,title):
    # videopage_url,img_url,title = mix
    # videopage_url = "http://www.68tmm.com:8888%s" %videopage_url
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=16d80d57701f3-0c620ed80071c8-1d3b6b55-1fa400-16d80d577024ad; Hm_lvt_79465e30fb78fd3df45b55fcbc3ee72b=1569824536; CNZZDATA1277477495=160265188-1569820341-%7C1569825788; AD_Time_480="idx:6"; Hm_lpvt_79465e30fb78fd3df45b55fcbc3ee72b=1569892650',
        'Host': 'www.68tmm.com:8888',
        'If-Modified-Since': 'Sun, 29 Sep 2019 10:21:06 GMT',
        'If-None-Match': 'W/"0d5749aaf76d51:0"',
        'Upgrade-Insecure-Requests': '1',
        'Referer''': 'http://www.68tmm.com:8888/diao/se28',
        'User-Agent': random.choice(UAPool_List)
    }

    print(video_url)
    
    try:
        respone = requests.get(video_url,headers=header)
    except Exception as ex:
        print('===========获取视频详情异常：%s================='%ex)
        print('===========重启获取视频详情=================')
        getVideoUrl(keyword, video_url, title)
        return
    
    if respone.status_code != 200 :
        print('网站响应失败！！！')
        return
    respone.encoding = 'gb2312'
    video_url = re.findall(r'video=\["(.*?)"',respone.text,re.S)[0]
    # print(video_url)
    downloadVideo(keyword,video_url,title)
   
def downloadList(keyword,info,process = 10):
    start_time = time.time()
    pool = multiprocessing.Pool(process)
    # array=[]
    for line in info:
        arr = line.split('@@@')
        video_url, title = arr
        # print(video_url, title)
        # download(video_url, title,10)
        pool.apply_async(getVideoUrl,(keyword,video_url, title, ))
    pool.close()
    pool.join()
    end_time = time.time()
    print('下载完毕,用时:%s秒' % (end_time - start_time))

def downloadVideo(keyword, video_url, title):

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'If-Modified-Since': 'Sun, 29 Sep 2019 10:21:06 GMT',
        'If-None-Match': 'W/"0d5749aaf76d51:0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(UAPool_List)
    }
    title += '.mp4'

    try:
        respone = requests.get(video_url, headers=header)
    except Exception as ex:
        print('===========下载视频异常：%s================='%ex)
        print('===========重启下载获取视频=================')
        downloadVideo(keyword, video_url,title)
        return
    
    if respone.status_code != 200 :
        print('网站响应失败！！！')
        return

    with open('/Users/leisure/Downloads/python_data/video/%s/%s'%(keyword,title), 'wb') as f:
        f.write(respone.content)
        print('下载完成：%s  地址：%s'%(title, video_url))


if __name__ == '__main__':
    getHomeList()