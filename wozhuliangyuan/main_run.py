from Girls import getGirls, getGirlsInfoByDB, getGirlYZ
from download import downloadList
from face_aip import getLocalImage
import os
import operator

if __name__ == "__main__":
    # 获取妹子数据
    # getGirls(1)
    path = '/Users/leisure/Desktop/meizi/'
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
    
    # 下载图片
    # girls = getGirlsInfoByDB()
    # downloadList(girls, 10)

    # 提交百度aipface识别
    # getLocalImage(path, 10)

    # 获取颜值列表数据
    listYZ = getGirlYZ()
    listTop = sorted(listYZ,key=operator.itemgetter('score'),reverse=True)
    # print(len(listTop))
    print(len(listTop))

    #筛选

