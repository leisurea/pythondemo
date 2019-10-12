from urllib import request
import gzip
import re
import base64
import os

baseUrl = 'http://10cilang1.com'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ec451dddb5d0ddafc72355d97e34a41c=1570697344; history=%5B%7B%22name%22%3A%22%E7%BD%91%E7%BA%A2%E7%BE%8E%E4%B9%B3%E8%90%9D%E8%8E%89%E5%B0%8F%E9%B8%9F%E9%85%B1%20%E4%BA%BA%E7%BE%8E%E9%80%BC%E7%BE%8E%20%E9%AB%98%E6%B8%85%E8%87%AA%E6%8B%8D%20%E6%8A%BD%E6%8F%92%22%2C%22pic%22%3A%22%2Fdetail%2F%3F9894.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F9894-0-0.html%22%2C%22part%22%3A%22%E7%AC%AC1%E9%9B%86%22%7D%5D; Hm_lpvt_ec451dddb5d0ddafc72355d97e34a41c=1570845432',
    'Host': '10cilang1.com',
    'Referer': 'http://10cilang1.com/list/?1.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
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
        req = request.Request(url=currUrl,headers=header,method='GET')
        respone = request.urlopen(req)
        xmldata = gzip.decompress(respone.read()).decode()
        #获取加密后的视频地址，interesting，找了半天
        base64PlayUrl = re.findall(r'var now=base64decode\("(.*?)"\)',xmldata,re.S)[0]
        #b'https://2.ddyunbo.com/20190718/K1SctSba/index.m3u8' 后面.decode()去掉b''
        base64PlayUrl = base64.b64decode(base64PlayUrl).decode()

        return base64PlayUrl
    except Exception as identifier:
        if '502' in repr(identifier) and retry > 5:
            return ''
        else:
            return getVideoPlayUrlFromDetailPage(video,retry)
        print('视频详情获取错误',repr(identifier))

# 上一步获取到的播放地址只是个头，里面内容才是真是的地址
# 分两种情况，一种获取到的是单m3u8,里面就是ts列表

# 另一种是先获取头部 EXT-X-STREAM-INF 的m3u8文件,里面有另一个m3u8的文件地址
# 另一个m3u8的文件地址又分两种情况，一种是直接1000k/hls/index.m3u8
# 另一种是/20190718/K1SctSba//800kb/hls/index.m3u8
# 先根据这个地址是否以/ 开头为判断拼接这第二个m3u8文件路径
def getm3u8Head(video, m3u8Url):
    try:
        # /video/?524-0-0.html
        referer = str(video[0]).replace('/video/?','').replace('.html','')
        referer = referer.split('-') # ['524', '0', '0']
        header = {
            'Origin': baseUrl,
            # 'Referer': 'http://10cilang1.com/js/player/dplayer/dplayer.html?videourl=/video/?524-0-0.html,https://qq.com-ixx-youku.com/20190831/6737_90f8f43e/index.m3u8,,524,0,0',
            'Referer': '{0}/js/player/dplayer/dplayer.html?{1},{2},,{3},{4},{5}'.format(baseUrl, video[0],m3u8Url,referer[0],referer[1],referer[2]),
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
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
            return getm3u8Head(video, nextM3U8Url)
        else:
            # 解析藏有完整ts地址列表的文件
            # 筛选出.ts文件列表, 筛选出来的结果是<class 'filter'>类型
            finalUrl = m3u8Url[0:m3u8Url.find('/',9,len(m3u8Url))]
            data = list(filter(lambda item: '.ts'in item,data))
            #再遍历一次，把地址补充完成，免得后续步骤忘记
            for i in range(len(data)):
                data[i] = finalUrl + data[i]
            return header, data
    except Exception as identifier:
        print('视频播放地址m3u8文件获取错误',repr(identifier))
        return getm3u8Head(video,m3u8Url)

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
def downloadTSFile(header, url):
    print(url)
    path = '/Users/leisure/Desktop/meizi3/测试/'
    filename = url[url.rfind('/')+1:]
    try:
        result = request.urlretrieve(url,'%s%s'%(path,filename))
        print('下载完成%s' %result[0])
        return result[0]
    except Exception as xiang:
        print('下载异常,重新下载：',xiang)
        downloadTSFile(header, url)
        return -1


#合并ts文件
def combine(path, file_name):
    file_list = file_walker(path)
    # file_path = combine_path + path.split('/')[-1] + file_name + '.ts'
    file_path = path + file_name + '.ts'
    # 排序
    file_list.sort()
    print(file_list)

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

    # getVideoPlayUrlFromDetailPage(('/video/?10703-0-0.html', '【萝莉】高清无码3p小萝莉连续中出淫水乱流3', 'http://10cilang1.com/list/?30.html'))
    # completeInfo = getm3u8Head(('/video/?10703-0-0.html', '【萝莉】高清无码3p小萝莉连续中出淫水乱流3', 'http://10cilang1.com/list/?30.html'),'https://2.ddyunbo.com/20190718/K1SctSba/index.m3u8')
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
    
    combine(path,'【萝莉】高清无码3p小萝莉连续中出淫水乱流3')
    # getFinalTSPlayUrl(m3u8Head)
    # video='/video/?524-0-0.html'
    # referer = str(video).replace('/video/?','').replace('.html','')
    # referer = referer.split('-')
    # print(type(referer[0]))