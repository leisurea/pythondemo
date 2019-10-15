import pymongo 
import random

#手动安装的数据库，麻烦的启动方法 mongod --config /usr/local/etc/mongod.conf
# 关闭 打开另一个终端窗口 切换到你的mongodb/bin目录下   ./mongo
#        > use admin
#         > db.shutdownServer()
# client = pymongo.MongoClient('mongodb://localhost')
client = pymongo.MongoClient(host='localhost',port=27017,connect=False)#数据库非线程安全，需要connect=False
database = client['Cilang_Video']#指定数据库
table = database['video']#集合。可以理解为表

def saveTSList(data):
    table.insert_one(data)
    print('保存数据成功')

def getTSList():
    return table.find()

#视频是否已经存在了
def isVideoExist(videoUrl):
    # resutl = table.find({'video':{'$elemMatch':{'a':videoUrl}}})
    resutl = table.find({},{'video'})
    for cur in resutl:
        if videoUrl in repr(cur):
            return True
    else:
        return False

#
if __name__ == "__main__":
    videoInfos = getTSList()
    # print(len(list(videoInfos)))
    for videoInfo in videoInfos:
        print(videoInfo['video'])


    # print(isVideoExist('/video/?10698-0-0.html'))



