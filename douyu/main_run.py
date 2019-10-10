from zhubo import getYZMeiZi,download
from face_aip import getFaceScore
import operator
import os

# 新的开始
def newStart():
    meizi = getYZMeiZi([], 1)
    print('逮到 %d 个颜值妹子主播信息' %len(meizi))
    for data in meizi:
        # 下载图片
        savePath = download(data['avatar'], data['name'])
        # 下载完成后
        if -1 == savePath:
            meizi.remove(data)
        score = getFaceScore(savePath)
        # 去除异常状况的妹子
        if score == -1:
            meizi.remove(data)

        #添加分数键值对
        data['score'] = score
    done(meizi)

# 图片下好了直接获取评分
def halfStart():
    meizi = []
    path = r'/users/leisure/desktop/meizi/'
    images = os.listdir(path)
    # print(images)
    for image in images:
        score = getFaceScore(path + image)
        print(image,' = ',score)
        # 去除异常状况的妹子
        if score == -1:
            continue

        #添加分数键值对
        meizi.append({'score':score, 'name': os.path.splitext(image)[0]})
    done(meizi)

def done(meizi):
    print(meizi)
    scored_meizi = sorted(meizi, key = operator.itemgetter('score'),reverse = True)
    print(meizi)
    print(scored_meizi)

if __name__ == "__main__":
   newStart()
    # halfStart()