import os
import platform
from mongodb import getTSList

#exec_str = r'copy /b  ts/c9645620628078.ts+ts/c9645620628079.ts  ts/1.ts'
#os.system(exec_str) 
# f = open('index.m3u8', 'r', encoding='utf-8')
# text_list = f.readlines()
# files = []
# for i in text_list:
#    if i.find('#EX')==-1:
#        files.append(i)
       
# f.close()


# tmp = []
# for file in files[0:450]:
#    tmp.append(file.replace("\n",""))
#    # 合并ts文件
# os.chdir("ts/")
# shell_str = '+'.join(tmp)
# #print(shell_str)
# shell_str = 'copy /b '+ shell_str + ' 5.mp4'

# os.system(shell_str)
# print(shell_str)

# 合并文件夹下所有文件
def mergeTS2MP4(path,outpath,outputName):
    files = file_walker(path)
    files.sort()
    # 切换到需要到输出目录
    os.chdir(outpath)
    # operation = r'copy /b '+ tmp + ' 湘儿.mp4' #windows下的命令
    # operation = 'cat '+ tmp + ' > 湘儿.mp4'

    if not outputName.endswith('.mp4'):
        outputName += '.mp4'

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        tmp = ' '.join(files)
        operation = 'cat '+ tmp + ' > ' + outputName
    else:
        tmp = '+'.join(files)
        operation = r'copy /b '+ tmp + ' ' + outputName #windows下的命令

    result = os.system(operation)
    if 0 == result:
        print('合并成功')
    else:
        print('合并失败')


# 获取目录下文件列表
def file_walker(path):
    file_list = []
    for root, dirs, files in os.walk(path): # a generator
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    return file_list

def isFileNameInFolder(existFiles, videoInfos, file):
    # print(existFiles,file)
    fileName = ''
    for videoInfo in videoInfos:
        if str(videoInfo["video"][0]).replace(r"/video/?",'').replace(r'.html','') == file:
            fileName = (videoInfo["video"][1]+'.mp4').replace(' ','_')
            print('存在 ',fileName)
            if fileName in existFiles:
                return videoInfo
    # print('xinager ',fileName, existFiles)
    # if '' != fileName and fileName in existFiles:
    #     print('存在',fileName)
    #     return True
    return None

def getVideoInfoByFolderName(videoInfos, folderName):
    for videoInfo in videoInfos:
        if str(videoInfo["video"][0]).replace(r"/video/?",'').replace(r'.html','') == folderName:
            return videoInfo
    return None

def isFileExist(existFiles, fileName):
    # print(existFiles, fileName)
    return fileName in existFiles
    

    
if __name__ == "__main__":
    path = '/Users/leisure/Downloads/cilang/'
    outpath = "/Volumes/TOSHIBA EXT/python/cldata/"
    # files = file_walker(path)
    # files.sort()
    # print(len(files+files))
    # mergeTS2MP4(path + '11560-0-0/', outpath ,'湘儿.mp4')

    videoInfos = getTSList()
    files = os.listdir(path)
    existFiles = os.listdir(outpath)

    xianger = []
    for videoInfo in videoInfos:
        xianger.append(videoInfo)
    # print(files)
    # print(existFiles)
    # print(existFiles[0])
    # print(files[0])

    for file in files:
        videoInfo = getVideoInfoByFolderName(xianger, file)
        if None != videoInfo:
            # if None != videoInfo and not isFileExist(existFiles, (videoInfo["video"][1]+'.mp4').replace(' ','_')):
            name = (videoInfo["video"][1]+'.mp4').replace(' ','_')
            if name not in existFiles:
                print(videoInfo["video"][0],' == ', name)
                mergeTS2MP4(path + str(videoInfo["video"][0]).replace(r"/video/?",'').replace(r'.html',''), outpath ,name)
            else:
                print('已经存在的文件：', name)
        else:
            print('不存在', file)



    # print(isFileNameInFolder(existFiles, videoInfos, files[1]))

    # for file in files:
    #     videoInfo = isFileNameInFolder(existFiles, videoInfos, file)
    #     if videoInfo != None:#不存在
            # for videoInfo in videoInfos:
            # print(videoInfo["video"][0],' == ', videoInfo["video"][1])
            # mergeTS2MP4(path + str(videoInfo["video"][0]).replace(r"/video/?",'').replace(r'.html',''), outpath ,(videoInfo["video"][1]+'.mp4').replace(' ','_'))
            # break
        # break


        
    # files.sort(key=lambda x: str(x.split('.')[0]))
    # print(files)
    # files.sort()

    # print(files)
    # for file in files:
    #     print(file)