from urllib import request
import gzip
import re

baseUrl = 'http://10cilang1.com/'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ec451dddb5d0ddafc72355d97e34a41c=1570697344; history=%5B%7B%22name%22%3A%22%E7%BD%91%E7%BA%A2%E7%BE%8E%E4%B9%B3%E8%90%9D%E8%8E%89%E5%B0%8F%E9%B8%9F%E9%85%B1%20%E4%BA%BA%E7%BE%8E%E9%80%BC%E7%BE%8E%20%E9%AB%98%E6%B8%85%E8%87%AA%E6%8B%8D%20%E6%8A%BD%E6%8F%92%22%2C%22pic%22%3A%22%2Fdetail%2F%3F9894.html%22%2C%22link%22%3A%22%2Fvideo%2F%3F9894-0-0.html%22%2C%22part%22%3A%22%E7%AC%AC1%E9%9B%86%22%7D%5D; Hm_lpvt_ec451dddb5d0ddafc72355d97e34a41c=1570780924',
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


#获取分类列表/list/?4.html
def getTabPage(tab, page):
    print('获取第%s页数据' %str(page))
    suffix = tab[0]+'-'+str(page)
    if page == 1:
        suffix = tab[0]

    currUrl = '{0}list/?{1}.html'.format(baseUrl,suffix)
    # http://10cilang1.com/list/?1-2.html
    header['Referer'] = 'http://10cilang1.com/list/?{0}.html'.format(tab[0])

    try:
        req = request.Request(url=currUrl,headers=header,method='GET')
        respone = request.urlopen(req)
        xmldata = gzip.decompress(respone.read()).decode()

        # url,title 
        li = re.findall(r'<h4 class="title text-overflow"><a href="(.*?)" title="(.*?)">',xmldata,re.S)
        print(li)
        totalPage = re.findall(r'<li class="visible-xs"><a class="btn btn-warm">(.*?)</a></li>',xmldata,re.S)[0]
        #['1/3']
        totalPage = str(totalPage).split('/')
        currPage = int(totalPage[0])#当前页码
        totalPage = int(totalPage[1])#总页数
        if currPage < totalPage:
            getTabPage(tab, currPage+1)
        else:
            pass
    except Exception as identifier:
        print('列表获取错误',repr(identifier))


if __name__ == "__main__":
    tabs = getHomeTabs()
    for tab in tabs:
        getTabPage(tab,1)
        break
