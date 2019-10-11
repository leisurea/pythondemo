import pymongo
from wordcloud import WordCloud
import jieba

# client = pymongo.MongoClient('mongodb://localhost')
client = pymongo.MongoClient(host='localhost',port=27017,connect=False)#数据库非线程安全，需要connect=False
girlsDB = client['WZLY_Girls']#指定数据库
girlsTB = girlsDB['girls']#集合。可以理解为表
girlsYZTB = girlsDB['girlsyz']#颜值数据库,因百度人脸识别成功率极低，故不与girls表合并

def showCloud(text):
    # text = ' '.join(jieba.cut(text,cut_all=False))

    # font_path须设置成中文字体，不然出现框框或空
    wordcloud=WordCloud(font_path='./lixu.ttf',background_color='black',width=600,height=300,max_words=50).generate(text)
    #3.生成图片
    image = wordcloud.to_image()
    # wordcloud.to_file('11.png')
    #4.显示图片
    image.show()

#云图
if __name__ == "__main__":
    # print(girlsYZTB.drop())
    # for girl in girlsYZTB.find():
        # print(girl)

    highYZ = girlsYZTB.find({'score':{'$gte':85}})
    highYZ = list(highYZ)
    print(len(highYZ))
    userid = []
    for girl in highYZ:
        # print(girl)
        userid.append(girl['userid'])

    highGirlInfo = girlsTB.find({'userid':{'$in':userid} ,'province':'广东'})
    # city = ''
    # province = ''
    # birthdayyear = ''
    # education = ''
    # height = ''
    # salary = ''
    for girl in highGirlInfo:
        print(girl)
    #     city += girl['city'] + ' '
    #     province += girl['province'] + ' '
    #     birthdayyear += girl['birthdayyear'] + '年 '#纯数字出错
    #     height += girl['height'] + 'CM '#纯数字出错
    #     education += girl['education'] + ' '
    #     salary += girl['salary'] + ' '

    # showCloud(city)
    # showCloud(province)
    # showCloud(education)
    # showCloud(birthdayyear)
    # showCloud(height)
    # showCloud(salary)



