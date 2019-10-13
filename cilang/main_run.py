
from VideoList import getHomeTabs, getTabPage, getVideoPlayUrlFromDetailPage, getm3u8Head
from mongodb import saveTSList, isVideoExist
import os

if __name__ == "__main__":
    # 获取栏目列表
    tabs = getHomeTabs()
    print('网站分类栏目共计获取到%d条数据'%len(tabs))
    for tab in tabs:
        # 获取栏目下所有视频列表
        lists = getTabPage([],tab,1)#video = url,title,referer
        print('%s 栏目共计获取到 %d 条数据'%(tab[1],len(lists)))
        for video in lists: 
            if isVideoExist(video[0]):
                continue
            base64PlayUrl = getVideoPlayUrlFromDetailPage(video)
            if '' == base64PlayUrl: #界面打不开，忽略
                continue
            else:
                # 获取视频详情数据
                m3u8Info = getm3u8Head(video, base64PlayUrl)
                if '' == m3u8Info:
                    continue
                header, tslist = m3u8Info
                print('%s 共计获取到 %d 条ts数据'%(video[1],len(tslist)))
                #保存一条视频数据到数据库
                saveTSList({'video':video,'header':header,'tslist':tslist})


    path = '/Users/leisure/Desktop/meizi3/'
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 