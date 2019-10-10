from aip import AipFace
import base64

""" 你的 APPID AK SK """
APP_ID = '17482590'
API_KEY = 'NefGW19DhQpg7MwFCtm7GrXa'
SECRET_KEY = 'lPjEeNF031CefvfkxvqGtROQ5qTj7vWz'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def getFaceScore(path):

    image = ''
    with open(path,'rb') as f:
        image = base64.b64encode(f.read()).decode()

    # image = "取决于image_type参数，传入BASE64字符串或URL字符串或FACE_TOKEN字符串"

    imageType = "BASE64"

    """ 调用人脸检测 """
    client.detect(image, imageType)

    """ 如果有可选参数 """
    options = {}
    options["face_field"] = "beauty"
    options["max_face_num"] = 1
    options["face_type"] = "LIVE"
    options["liveness_control"] = "LOW"

    try:
        """ 带参数调用人脸检测 """
        result = client.detect(image, imageType, options)
        # print(result)
        # 获取颜值分数
        socre = result['result']['face_list'][0]['beauty']
        # print(socre)
        return socre
    except Exception :
        return -1
    

if __name__ == "__main__":
    getFaceScore('/users/leisure/desktop/meizi/xianger.jpg')


