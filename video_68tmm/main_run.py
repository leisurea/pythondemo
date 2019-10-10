from download_list import getHomeList,getVideoUrl,downloadList
from search import search,getVideoInfo
from collections import defaultdict
import os



if __name__ == '__main__':
    # 读取网页列表并存储数据到本地
    # getHomeList()

    keyword = '动漫'
    # 先创建目录
    path = '/Users/leisure/Downloads/python_data/video/%s/' %(keyword)
    folder = os.path.exists(path)
    #判断结果
    if not folder:
        #如果不存在，则创建新目录
        os.makedirs(path)

    # #搜索下载文件
    search(keyword)
    # #获取本地视频列表
    info = getVideoInfo(keyword)
    downloadList(keyword,info,10)


   

