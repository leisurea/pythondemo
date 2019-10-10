#获取主播列表
import urllib.request
import json
from io import BytesIO
import gzip

url = 'https://www.douyu.com/gapi/rknc/directory/yzRec/'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'dy_did=83759b94ef0186aefed112be00061501; acf_did=83759b94ef0186aefed112be00061501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1570614026; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1570672149',
    'referer': 'https://www.douyu.com/g_yz',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

#获取颜值主播列表
def getYZMeiZi(meizi, page):
    req = urllib.request.Request(url = url + str(page), headers = headers, method = 'GET')
    respone = urllib.request.urlopen(req)
    # gzip编码的，转换一下,或者直接用requests
    # 方法一
    # buff = BytesIO(respone.read())
    # f = gzip.GzipFile(fileobj=buff)
    # print(f.read().decode('utf-8'))
    # 方法二
    data = gzip.decompress(respone.read()).decode()
    # print(data)
    resutl = json.loads(data)
    # print(resutl['data']['pgcnt'])
    # print(len(resutl['data']['rl']))
    for rl in resutl['data']['rl']:
        name = rl['nn']
        tag = rl['rn']
        rid = rl['rid']
        avatar = str(rl['rs16']).replace('/dy1','')
        meizi.append({'name' : name, 'tag' : tag, 'rid' : rid, 'avatar' : avatar})

    # print('====%d===='%page,meizi)
    totalPage = resutl['data']['pgcnt']
    # 浏览下一页
    if page < totalPage:
        return getYZMeiZi(meizi, page + 1)
    else:
        return meizi


#url的形式百度无法识别，只能下载了再上传，interesting
def download(image, name):
    # req = urllib.request.Request(image,headers = header2)
    # respone = urllib.request.urlopen(req)
    # data = respone.read().decode()
    try:
        result = urllib.request.urlretrieve(image,'/Users/leisure/Desktop/meizi/%s.jpg'%name)
        print('下载完成%s' %result[0])
        return result[0]
    except Exception:
        return -1


if __name__ == "__main__":
   meizi= getYZMeiZi([], 1)
   print(meizi)