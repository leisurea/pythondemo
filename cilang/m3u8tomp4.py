import os
import platform

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

if __name__ == "__main__":
    path = '/Users/leisure/Downloads/cilang/'
    # files = file_walker(path)
    # files.sort()
    # print(len(files+files))
    mergeTS2MP4(path+'11750-0-0/', path ,'湘儿.mp4')


    # files = os.listdir(path)
    # print(files)
    # files.sort(key=lambda x: str(x.split('.')[0]))
    # print(files)
    # files.sort()

    # print(files)
    # for file in files:
    #     print(file)