from aip import AipFace
import base64
import os
import multiprocessing
import time
from Girls import saveGirlYZ

""" 你的 APPID AK SK """
APP_ID = '17482590'
API_KEY = 'NefGW19DhQpg7MwFCtm7GrXa'
SECRET_KEY = 'lPjEeNF031CefvfkxvqGtROQ5qTj7vWz'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

""" 如果有可选参数 """
options = {}
options["face_field"] = "beauty"
# options["max_face_num"] = 1
# options["face_type"] = "LIVE"
# options["liveness_control"] = "LOW"

#获取本地图片，转成base64上传，传url不可
# 注意，不要开线程，不然成功率只有10%左右
def getLocalImage(path, process=10):
    images = os.listdir(path)
    start_time = time.time()
    pool = multiprocessing.Pool(process)

    for image in images:
        # print(image)
        if process == 1:
            getFaceScore(path, image)
        else:
            pool.apply_async(getFaceScore,(path, image, ))
    pool.close()
    pool.join()
    end_time = time.time()
    print('分析完毕,用时:%s秒' % (end_time - start_time))


# 上传图片，获取分数
def getFaceScore(path, imageName):
    image = ''
    with open(path+imageName,'rb') as f:
        image = base64.b64encode(f.read()).decode()

    imageType = "BASE64"

    """ 调用人脸检测 """
    client.detect(image, imageType)

    try:
        """ 带参数调用人脸检测 """
        result = client.detect(image, imageType, options)
        # print(result)
        # 获取颜值分数
        socre = result['result']['face_list'][0]['beauty']
        userid = imageName.replace('.jpg','')
        print('userid:%s : 分数：%d'%(userid,socre))
        saveGirlYZ({'userid': userid, 'score':socre})
        return socre
    except Exception as xiang:
        print('%s识别异常：'%imageName, repr(xiang))
        return -1
    

# if __name__ == "__main__":
    # print(getFaceScore('/users/leisure/desktop/meizi/阮绵绵童鞋.jpg'))


