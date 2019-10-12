import pymongo

# client = pymongo.MongoClient('mongodb://localhost')
client = pymongo.MongoClient(host='localhost',port=27017,connect=False)#数据库非线程安全，需要connect=False
database = client['Cilang_Video']#指定数据库
table = database['video']#集合。可以理解为表

def saveTSList(data):
    table.insert_one(data)
    print('保存数据成功')

def getTSList():
    return table.find()

#
if __name__ == "__main__":
    videoInfos = getTSList()
    for videoInfo in videoInfos:
        print(videoInfo['video'])



