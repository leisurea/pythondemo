import urllib.request
import time
import multiprocessing

#url的形式百度无法识别，只能下载了再上传，interesting
def download(path, image, name):
    # req = urllib.request.Request(image,headers = header2)
    # respone = urllib.request.urlopen(req)
    # data = respone.read().decode()
    try:
        result = urllib.request.urlretrieve(image,'%s%s.jpg'%(path,name))
        print('下载完成%s' %result[0])
        return result[0]
    except Exception as xiang:
        print('下载异常：',xiang)
        return -1

def downloadList(path, girls, process = 10):
    start_time = time.time()
    pool = multiprocessing.Pool(process)

    for girl in girls:
        pool.apply_async(download,(path, girl['avatar'], girl['userid'], ))
    pool.close()
    pool.join()
    end_time = time.time()
    print('下载完毕,用时:%s秒' % (end_time - start_time))

# if __name__ == "__main__":
    # download('http://img.7799520.com/c1737163-516e-4be8-bf4f-d19ec48a26b9','陆地章小鱼')