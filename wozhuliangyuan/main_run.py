from Girls import getGirls, getGirlsInfoByDB, getGirlYZ
from download import downloadList
from face_aip import getLocalImage
import os
import operator
import platform


if __name__ == "__main__":
    
    path = '/Users/leisure/Desktop/meizi2/'
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 

    # 获取妹子数据
    # getGirls(1)
    # # 下载图片
    # girls = getGirlsInfoByDB()
    # downloadList(path, girls, 10)

    # 提交百度aipface识别
    getLocalImage(path, 1)

    # 获取颜值列表数据前10名
    listYZ = getGirlYZ()
    listTop = sorted(listYZ,key=operator.itemgetter('score'),reverse=True)
    # print(listTop)
    print(len(listTop))

    userPlatform = platform.system()						# 获取操作系统

    for i in range(10):
        fileDir = path + listTop[i]['userid'] + '.jpg'
         
        if userPlatform == 'Darwin':								# Mac
            platform.subprocess.call(['open', fileDir])
        elif userPlatform == 'Linux':								# Linux
            platform.subprocess.call(['xdg-open', fileDir])
        # else:														# Windows
            # os.startfile(fileDir)

    #筛选

