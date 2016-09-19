from spider import SpiderHTML
from multiprocessing import Pool
import sys,urllib,http,os,random,re,time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Firefox()
# driver.implicitly_wait(5) # seconds
# driver.get("http://www.bilibili.com/video/av6315006/")
# dm = driver.find_element_by_id('dm_count')
# print(dm.text)
# exit()

__author__ = 'waiting'


driver = webdriver.Firefox()
driver.implicitly_wait(5) # seconds

# orders = {"hot":"播放量","review":"评论数","promote":"硬币数","stow":"收藏数"}
orders = {"promote":"硬币数"}
biliUrl = 'http://www.bilibili.com'
#module 为 分类 :游戏 game 舞蹈 dance等
pattern = re.compile(r'(\d+)')

class BilibiliSpider(SpiderHTML):
    def __init__(self,module,timeStart,timeEnd):
        self.url = biliUrl + '/video/' + module + '.html'
        self.timeStart = timeStart
        self.timeEnd = timeEnd

    def start(self):
        content = self.getUrl(self.url)
        sorts = content.find('ul',class_='n_num')
        subSorts = sorts.find_all('a')
        
        #处理该类别下的子模块
        for sub in subSorts:
            subName = sub.string
            if(subName == '全部'):
                continue
            #子模块只需要tid即可
            tid = sub.parent['tid']
            if tid is None or tid == '' :
                print('模块{type} tid解析错误'.format(type=subName))
                continue
            self.parsePage(subName,tid)

    #处理一个子模块的页面
    def parsePage(self,typeName,tid):
        for (order,name) in orders.items():
            sumData = dict()
            print("对子模块‘{typeName}’进行‘{name}’模块的分析".format(name=name,typeName=typeName))
            sort = 0;
            for page in (1,):
                # http://www.bilibili.com/list/stow-65-1-2016-09-12~2016-09-19.html
                urlTmp = biliUrl + "/list/{order}-{tid}-{page}-{start}~{end}.html".format(order=order,tid=tid,page=page,start=self.timeStart,end=self.timeEnd)
                content = self.getUrl(urlTmp)

                videoContent = content.find('ul',class_='vd-list l1')
                videoList = videoContent.find_all('div',class_='l-item')
                
                for video in videoList:
                    AVInfo = dict()     #作品信息
                    # print(video)
                    AVInfo['title'] = video.find('a',class_='title').string                     #标题
                    AVInfo['name'] = video.find('a',class_='v-author').string                   #作者
                    AVInfo['play'] = video.find('span',class_='v-info-i gk').span.string        #播放数
                    AVInfo['danmu'] = video.find('span',class_='v-info-i dm').span.string       #弹幕数
                    AVInfo['collect'] = video.find('span',class_='v-info-i sc').span.string     #收藏数
                    AVInfo['url'] = biliUrl + video.find('a',class_='title')['href']            #视频链接
                    AVInfo['desc'] = video.find('div',class_='v-desc').string                   #视频描述
                    AVInfo['id'] = video.find('a',class_='v-author')['href'].split('/')[-1]     #用户id

                    coinInfo = self.parseAV(video.find('a',class_='title')['href'])
                    sort=sort+1
                    if coinInfo == 0:
                        sumData = self.renderData(sumData,AVInfo)
                        print("排名第{sort}：\t{name},\t播放量:{play},\t收藏数:{collect},\t作品名：{title},【视频信息已消失，无法获取更多信息】".format(sort=sort,**AVInfo))    
                        continue
                    #合并信息
                    AVInfo = dict(coinInfo,**AVInfo)
                    sumData = self.renderData(sumData,AVInfo)
                    print("排名第{sort}：\t{name},\t播放量:{play},\t收藏数:{collect},\t硬币数:{coin},\t作品名：{title}".format(sort=sort,**AVInfo))
                    # if sort==5:
                    #     break
            print(sumData)
            for (uid,data) in sumData.items():
                print("汇总数据:\t{name},\t播放量:{play},\t收藏数:{collect},\t".format(**data))
                    

    #解析单独的一个视频
    # @param avNum String video/av6315006/
    def parseAV(self,avNum):
        url = biliUrl + avNum
        info = dict()
        try:
            driver.get(url)
            shareElement = driver.find_element_by_xpath("//div[@class='block share initialized']/span[1]/div[1]/span[2]")
            info['share'] = shareElement.text   #分享数
            coinElement = driver.find_element_by_xpath("//div[@class='block coin']/span[1]/div[1]/span[2]")
            info['coin'] = coinElement.text   #硬币数
        except:
            return 0
        # url = "http://api.bilibili.com/archive_stat/stat?callback=jQuery1720020664264156293077_1474269696982&aid={aid}&type=jsonp&_={time}".format(aid=aid,time=timeStamp)
        # content = self.getUrl(url)
        # print(content)
        
        return info

    #数据汇总
    def renderData(self,data,info):
        try:
            data[info['id']]['play'] = int(data[info['id']]['play']) + int(info['play'])
            data[info['id']]['danmu'] = int(data[info['id']]['danmu']) + int(info['danmu'])
            data[info['id']]['collect'] = int(data[info['id']]['collect']) + int(info['collect'])
        except KeyError:
            data[info['id']] = dict()
            data[info['id']]['play'] = info['play']
            data[info['id']]['danmu'] = info['danmu']
            data[info['id']]['collect'] = info['collect']
            data[info['id']]['name'] = info['name']
        return data


start = '2016-08-01'
end = '2016-08-31'
spider = BilibiliSpider('game',start, end)
print("分析周期：`{start}` ~ `{end}`".format(start=start,end=end))
spider.start()

