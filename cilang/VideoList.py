from urllib import request
import gzip
import re
import base64
import os
import random
import sys
import time
#必须放在外部模块引用前面，干
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)

from util.UAPool import data as UserAgent
import ssl
import socket

# context = ssl._create_unverified_context()
# response = request.urlopen(request,context=context)
# ssl._create_default_https_context = ssl._create_unverified_context

socket.setdefaulttimeout(30)

baseUrl = 'http://10cilang2.com'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ec451dddb5d0ddafc72355d97e34a41c=1572140272; history=%5B%7B%22name%22%3A%22%E6%97%A6%E9%82%A3%E3%81%8C%E5%B8%B0%E3%81%A3%E3%81%A6%E3%81%8D%E3%81%A6%EF%BC%93%EF%BC%B0%E4%B9%B1%E4%BA%A4%E3%81%A7%E4%BD%95%E5%BA%A6%E3%82%82%E3%82%A4%E3%81%A3%E3%81%A1%E3%82%83%E3%81%86%20o%E7%95%AA%E5%8F%B7%EF%BC%9At415%22%2C%22pic%22%3A%22%2Fdetail%2F%3F7038.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F7038-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22%E6%B7%AB%E4%B9%B1%E7%BE%8E%E4%BA%BA%E3%83%8F%E3%83%BC%E3%83%95%E3%82%92%E3%81%BE%E3%82%93%E3%81%90%E3%82%8A%E8%BF%94%E3%81%97%E3%81%A7%E5%A4%A7%E9%87%8F%E6%BD%AE%E5%90%B9%E3%81%8D%20%E7%95%AA%E5%8F%B7%EF%BC%9Aubt1004%22%2C%22pic%22%3A%22%2Fdetail%2F%3F7067.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F7067-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22%E5%A6%B9%E7%B3%BB%E3%81%AA%E5%A5%B3%E5%AD%90%E6%A0%A1%E7%94%9F%E3%83%9E%E3%83%B3%E3%82%B3%E3%81%AB%E4%B8%AD%E5%87%BA%E3%81%97%20%E7%95%AA%E5%8F%B7%EF%BC%9Aot435%22%2C%22pic%22%3A%22%2Fdetail%2F%3F7086.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F7086-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22%E3%82%B9%E3%82%AD%E3%83%A2%E3%83%8E%E6%B7%AB%E4%B9%B1%E4%BA%BA%E5%A6%BB%E3%82%92%E5%AF%86%E5%AE%A4%E7%8B%AC%E3%82%8A%E5%8D%A0%E3%82%81-2%20%E7%95%AA%E5%8F%B7%EF%BC%9Aheyzo_hd_0614_full%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11582.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11582-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22Z%EF%BD%9E%E3%82%AE%E3%83%A3%E3%83%AB%E3%81%AE%E3%83%9C%E3%83%87%E3%82%A3%E3%82%92%E5%AE%8C%E5%85%A8%E6%80%A7%E8%A6%87-2%20%E7%95%AA%E5%8F%B7%EF%BC%9Aheyzo_hd_1943_full%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11397.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11397-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22%E6%9E%81%E5%93%81%E9%AB%98%E9%A2%9C%E5%80%BC%E6%A8%A1%E7%89%B9%E5%85%BC%E8%81%8C%E5%8D%96%E6%B7%AB%E5%A5%B3%E5%92%8C%E5%A4%A7%E6%AC%BE%E9%85%92%E5%BA%97%E5%BC%80%E6%88%BF%E5%90%84%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11662.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11662-0-0.html%22%2C%22part%22%3A%22%E7%AC%AC1%E9%9B%86%22%7D%2C%7B%22name%22%3A%22%E9%9D%9E%E5%B8%B8%E9%AA%9A%E6%B0%94%E7%9A%84%E7%86%9F%E5%A5%B3%E4%B8%BB%E6%92%AD%E6%89%AD%E5%8A%A8%E5%B0%8F%E8%9B%AE%E8%85%B0%E7%8E%B0%E5%9C%BA%E7%9B%B4%E6%92%AD%E8%B7%B3%E8%9B%8B%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11666.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11666-0-0.html%22%2C%22part%22%3A%22%E7%AC%AC1%E9%9B%86%22%7D%2C%7B%22name%22%3A%22Hamar%2Fs%20World%2016%20part1-4%20%E7%95%AA%E5%8F%B7%EF%BC%9Aheyzo_hd_0650%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11941.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11941-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22Sun%20Will%20Shine%20World-1%20%E7%95%AA%E5%8F%B7%EF%BC%9AQ8199%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11563.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11563-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%2C%7B%22name%22%3A%22%E5%B8%AB%E7%BE%8E%E4%BA%BA%E7%9C%8B%E8%AD%B7%E5%B8%AB%E3%81%AF%E3%83%95%E3%82%A7%E3%83%A9%E3%83%81%E3%82%AA%E3%81%AE%E9%81%94%E4%BA%BA-2%20%E7%95%AA%E5%8F%B7%EF%BC%9A101519_914-1pon-1080p%22%2C%22pic%22%3A%22%2Fdetail%2F%3F11718.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F11718-0-0.html%22%2C%22part%22%3A%22%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE%22%7D%5D; Hm_lpvt_ec451dddb5d0ddafc72355d97e34a41c='+str(int(time.time())),
    # 'Host': '10cilang2.com',
    'Referer': 'http://10cilang2.com/list/?1.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UserAgent)
}

#获取首页频道列表
def getHomeTabs():
    try:
        req = request.Request(url=baseUrl,headers=header,method='GET')
        respone = request.urlopen(req)
        xmldata = gzip.decompress(respone.read()).decode()
        
        tabs = re.findall(r'<ul class="item nav-list clearfix">(.*?)</ul>',xmldata,re.S)[0]
        # type, typename
        li = re.findall(r'<a class="btn btn-sm btn-block btn-" href="/list/\?(.*?).html">(.*?)</a>',tabs,re.S)
        # print(li)
        return li
    except Exception as identifier:
        print('首页tab列表获取错误',repr(identifier))


#获取频道下全部子列表/list/?4.html
def getTabPage(lists, tab, page):
    # print('获取频道 %s 下第 %s 页数据' %(tab[1],str(page)))
    suffix = tab[0]+'-'+str(page)
    if page == 1:
        suffix = tab[0]

    currUrl = '{0}/list/?{1}.html'.format(baseUrl,suffix)
    # http://10cilang1.com/list/?1-2.html
    header['Referer'] = '{0}/list/?{1}.html'.format(baseUrl, tab[0])
    header['User-Agent'] = random.choice(UserAgent)

    try:
        req = request.Request(url=currUrl,headers=header,method='GET')
        respone = request.urlopen(req)
        xmldata = gzip.decompress(respone.read()).decode()

        # url,title 
        li = re.findall(r'<h4 class="title text-overflow"><a href="(.*?)" title="(.*?)">',xmldata,re.S)
        # print(li)
        #这种方式无法修改
        # for tup in li:
        #     tup+=(currUrl,)
        for i in range(len(li)):
            li[i] += (currUrl,) # 添加当前地址到列表，获取视频详情界面用到referer
        lists += li # 添加数据到列表
        totalPage = re.findall(r'<li class="visible-xs"><a class="btn btn-warm">(.*?)</a></li>',xmldata,re.S)[0]
        #['1/3']
        totalPage = str(totalPage).split('/')
        currPage = int(totalPage[0])#当前页码
        totalPage = int(totalPage[1])#总页数
        if currPage < totalPage:
            return getTabPage(lists, tab, currPage+1)
        else:
            return lists
    except Exception as identifier:
        print('列表获取错误并重试：',repr(identifier))
        return getTabPage(list, tab, currPage)

# 获取视频详情里的播放地址 video('/video/?10703-0-0.html',title,referer)
def getVideoPlayUrlFromDetailPage(video,retry = 0):
    currUrl = baseUrl + video[0]
    try:
        header['Referer'] = video[2]
        header['User-Agent'] = random.choice(UserAgent)

        req = request.Request(url=currUrl,headers=header,method='GET')
        respone = request.urlopen(req)
        xmldata = gzip.decompress(respone.read()).decode()
        #获取加密后的视频地址，interesting，找了半天
        base64PlayUrl = re.findall(r'var now=base64decode\("(.*?)"\)',xmldata,re.S)[0]
        #b'https://2.ddyunbo.com/20190718/K1SctSba/index.m3u8' 后面.decode()去掉b''
        base64PlayUrl = base64.b64decode(base64PlayUrl).decode()

        return base64PlayUrl
    except Exception as identifier:
        print('%s视频详情获取错误'%str(video[1]),repr(identifier))
        # if ('502' in repr(identifier) or '403' in repr(identifier)) and retry > 2:
        if retry > 1:
            return ''
        else:
            return getVideoPlayUrlFromDetailPage(video,retry+1)
       

# 上一步获取到的播放地址只是个头，里面内容才是真是的地址
# 分两种情况，一种获取到的是单m3u8,里面就是ts列表

# 另一种是先获取头部 EXT-X-STREAM-INF 的m3u8文件,里面有另一个m3u8的文件地址
# 另一个m3u8的文件地址又分两种情况，一种是直接1000k/hls/index.m3u8
# 另一种是/20190718/K1SctSba//800kb/hls/index.m3u8
# 先根据这个地址是否以/ 开头为判断拼接这第二个m3u8文件路径
def getm3u8Head(video, m3u8Url,retry=0):
    try:
        # /video/?524-0-0.html
        referer = str(video[0]).replace('/video/?','').replace('.html','')
        referer = referer.split('-') # ['524', '0', '0']
        header = {
            'Origin': baseUrl,
            # 'Referer': 'http://10cilang1.com/js/player/dplayer/dplayer.html?videourl=/video/?524-0-0.html,https://qq.com-ixx-youku.com/20190831/6737_90f8f43e/index.m3u8,,524,0,0',
            'Referer': '{0}/js/player/dplayer/dplayer.html?{1},{2},,{3},{4},{5}'.format(baseUrl, video[0],m3u8Url,referer[0],referer[1],referer[2]),
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': random.choice(UserAgent)
        }
        req = request.Request(url=m3u8Url,headers=header,method='GET')
        respone = request.urlopen(req).read().decode()
        #第一种情况


        #第二种情况
        # #EXTM3U
        # EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=720x540
        # /20190718/K1SctSba//800kb/hls/index.m3u8
        data = respone.split('\n')
        
        if 'EXT-X-STREAM-INF' in str(data[1]):
            #第二种情况，即两个m3u8文件
            nextM3U8Url = getNextM3U8CompleteUrl(m3u8Url,data[2])
            # print(nextM3U8Url)
            return getm3u8Head(video, nextM3U8Url)
        else:
            # 解析藏有完整ts地址列表的文件
            # 筛选出.ts文件列表, 筛选出来的结果是<class 'filter'>类型
            # finalUrl = m3u8Url[0:m3u8Url.find('/',9,len(m3u8Url))]#抓取错误
            finalUrl = m3u8Url.replace('index.m3u8','')
            data = list(filter(lambda item: '.ts'in item,data))
            #再遍历一次，把地址补充完成，免得后续步骤忘记
            for i in range(len(data)):
                data[i] = finalUrl + data[i]
            # print(data[0])
            return header, data
    except Exception as identifier:
        print('%s视频播放地址m3u8文件获取错误'%str(video[1]),repr(identifier))
        # if '403' in repr(identifier) and retry > 5:#404也出来了
        if retry > 1:
            return ''
        else:
            return getm3u8Head(video,m3u8Url,retry+1)
        # print('视频播放地址m3u8文件获取错误',repr(identifier))
        # return getm3u8Head(video,m3u8Url)

# 根据第一个m3u8文件获取到的第二个m3u8地址后缀拼凑成完整的第二个m3u8地址
def getNextM3U8CompleteUrl(lastUrl, suffixUrl):
    # url = 'https://qq.com-ixx-youku.com/20190831/6737_90f8f43e/index.m3u8'
    # data = '1000k/hls/index.m3u8'
    if suffixUrl.startswith('/'):
        lastUrl = lastUrl[0:lastUrl.find('/',9,len(lastUrl))]
    else:
        lastUrl = lastUrl[:lastUrl.rfind('/')+1]

    return lastUrl + suffixUrl

# 下载ts列表文件
def downloadTSFile(path, header, url,retry = 0):
    # path = '/Users/leisure/Desktop/meizi3/测试/'
    filename = url[url.rfind('/')+1:]
    try:
        opener = request.build_opener()
        # opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER')]
        opener.addheaders = header
        request.install_opener(opener)
        result = request.urlretrieve(url,'%s%s'%(path, filename))
        print('下载完成%s' %result[0])
        return result[0]
    except Exception as xiang:
        print('下载异常,重新下载：',xiang, url)
        # return -1
        if retry > 2:
            return -1
        else:
            return downloadTSFile(path, header, url,retry+1)


#合并ts文件
def combine(path, file_name):
    file_list = file_walker(path)
    # file_path = combine_path + path.split('/')[-1] + file_name + '.ts'
    file_path = path + file_name + '.ts'
    # 排序
    file_list.sort()
    # print(file_list)

    with open(file_path, 'wb+') as fhand:
        for i in range(len(file_list)):
            f = file(file_list[i], 'rb')
            fhand.write(f.read())
            f.close()

def file(path, way):
    return open(path,way)

def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path): # a generator
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    return file_list

if __name__ == "__main__":
    # tabs = getHomeTabs()
    # for tab in tabs:
    #     lists = getTabPage([],tab,1)
    #     print('获取tab数据完成：', tab, '共计 %s 条'%str(len(lists)))
    #     # print(lists)
    #     break

   #  header, data = completeInfo
    path = '/Users/leisure/Desktop/meizi3/'
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path) 

    path += '测试'+'/'
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path) 
    # for url in data:
    #     downloadTSFile(header,url)
    
    # getFinalTSPlayUrl(m3u8Head)
    # video='/video/?524-0-0.html'
    # referer = str(video).replace('/video/?','').replace('.html','')
    # referer = referer.split('-')
    # print(type(referer[0]))