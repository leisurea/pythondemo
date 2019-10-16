
from VideoList import getHomeTabs, getTabPage, getVideoPlayUrlFromDetailPage, getm3u8Head,downloadTSFile
from mongodb import saveTSList, isVideoExist,getTSList
from m3u8tomp4 import mergeTS2MP4
import os
import time
import multiprocessing

#创建文件夹
def makedir(path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 

# 下载一部视频并且合并
def downloadOneVideo(videoInfo,path):
    start_time = time.time()
    pool = multiprocessing.Pool(10)

    filePath = path + videoInfo['video'][0].replace('/video/?','').replace('.html','')+'/'
    
    if os.path.exists(filePath):
        print('已经存在的目录不下载', filePath)
        return

    makedir(filePath)
    fileName = videoInfo['video'][1] + '.mp4'
    tslist = videoInfo['tslist']
    header = videoInfo['header']
    # print(tslist)
    # print(repr(videoInfo))
    results = []
    for url in tslist:
        results.append(pool.apply_async(downloadTSFile,(filePath, header, url,)))
        # pool.apply_async(download,(path, girl['avatar'], girl['userid'], ))
    pool.close()
    pool.join()
    end_time = time.time()
    print('下载完毕,用时:%s秒,共计下载%d条数据' % (end_time - start_time,len(results)))

    mergeTS2MP4(filePath, path, fileName)


if __name__ == "__main__":
    # 获取栏目列表
    tabs = getHomeTabs()
    print('网站分类栏目共计获取到%d条数据'%len(tabs))
    for tab in tabs:
        if '有码' in tab[1]:
            continue
        # 获取栏目下所有视频列表
        lists = getTabPage([],tab,1)#video = url,title,referer
        print('%s 栏目共计获取到 %d 条数据'%(tab[1],len(lists)))
        for video in lists: 
            if isVideoExist(video[0]):
                continue
            base64PlayUrl = getVideoPlayUrlFromDetailPage(video)
            print(base64PlayUrl)
            if '' == base64PlayUrl: #界面打不开，忽略
                continue
            elif base64PlayUrl.endswith('.mp4'):
                #直接暴露地址了
                continue
            else:
                # 获取视频详情数据
                m3u8Info = getm3u8Head(video, base64PlayUrl)
                if '' == m3u8Info:
                    continue
                header, tslist = m3u8Info
                print('%s 共计获取到 %d 条ts数据'%(video[1],tslist))
                #保存一条视频数据到数据库
                # saveTSList({'video':video,'header':header,'tslist':tslist})
                # break
        # break

    # path = '/Users/leisure/downloads/cilang/'
    # makedir(path)
    # #获取所有视频列表
    # videoInfos = getTSList()
    # # print(len(list(videoInfos)))
    # for videoInfo in videoInfos:
    #     downloadOneVideo(videoInfo,path)
