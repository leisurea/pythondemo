from urllib import request
import gzip
import json
import pymongo

url = 'http://www.7799520.com/api/user/pc/list/search?startage=21&endage=30&gender=2&marry=1&education=40&page='
header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ee0de768b7db1b355930288073352dbe=1570697708,1570697723; 59167___602875_KS_59167___602875=533e0a4197d947c2a78a75b6914e339f; 59167___602875_KS_ri_ses=19110379583%7CA5A8617FD5C8D5C93836B44DF55F9C9B-null; 59167___602875_curPageNum=1; Hm_lpvt_ee0de768b7db1b355930288073352dbe=1570698035',
    'Host': 'www.7799520.com',
    'Referer': 'http://www.7799520.com/jiaoyou.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

client = pymongo.MongoClient('mongodb://localhost')
girlsDB = client['WZLY_Girls']#指定数据库
girlsTB = girlsDB['girls']#集合。可以理解为表
girlsYZTB = girlsDB['girlsyz']#颜值数据库（需要优化）

# 获取列表，默认一页10条记录，没有发现总页数限制,先获取100页试试
def getGirls(page):
    try:
        req = request.Request(url=url+str(page),headers=header,method='GET')
        respone = request.urlopen(req)
        data = gzip.decompress(respone.read()).decode()
        resutl = json.loads(data)
        # print(resutl)
        items = resutl['data']['list']
        girlsTB.insert_many(items)
        # for item in items:
        if page < 100:
            print('第%d页完成：'%page)
            getGirls(page+1)
    except Exception as identifier:
        print('第%d页报错：'%page, identifier)

def getGirlsInfoByDB():
    return girlsTB.find()

# 保存颜值数据
def saveGirlYZ(yanzhi):
    girlsYZTB.insert_one(yanzhi)

def getGirlYZ():
    return girlsYZTB.find()

if __name__ == "__main__":
    # getGirls(1)
    print(girlsTB.find_one()['username'])
    # for item in girlsTB.find():
    #     print(item)
