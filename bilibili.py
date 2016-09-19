from spider import SpiderHTML
from multiprocessing import Pool
import sys,urllib,http,os,random,re,time
__author__ = 'waiting'

orders = {"hot":"播放量","review":"评论数","promote":"硬币数","stow":"收藏数"}

biliUrl = 'http://www.bilibili.com'
#module 为 分类 :游戏 game 舞蹈 dance等
# pattern = re.compile(r'av(\d+)')
# print(int(time.time()*1000))
# # aid = re.search(pattern,"/video/av5685228/")
# aid = pattern.search("/video/av5685228/")
# print(aid.group()) 
# exit()
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

    def parsePage(self,typeName,tid):
        for (order,name) in orders.items():
            print("对子模块‘{typeName}’进行‘{name}’模块的分析".format(name=name,typeName=typeName))
            for page in (1,2):
                # http://www.bilibili.com/list/stow-65-1-2016-09-12~2016-09-19.html
                urlTmp = biliUrl + "/list/{order}-{tid}-{page}-{start}~{end}.html".format(order=order,tid=tid,page=page,start=self.timeStart,end=self.timeEnd)
                content = self.getUrl(urlTmp)

                videoContent = content.find('ul',class_='vd-list l1')
                videoList = videoContent.find_all('div',class_='l-item')
                for video in videoList:
                    AVInfo = dict()     #作品信息
                    AVInfo['title'] = video.find('a',class_='title').string                     #标题
                    AVInfo['name'] = video.find('a',class_='v-author').string                   #作者
                    AVInfo['play'] = video.find('span',class_='v-info-i gk').span.string        #播放数
                    AVInfo['danmu'] = video.find('span',class_='v-info-i dm').span.string       #弹幕数
                    AVInfo['collect'] = video.find('span',class_='v-info-i sc').span.string     #收藏数
                    AVInfo['url'] = biliUrl + video.find('a',class_='title')['href']            #视频链接
                    AVInfo['desc'] = video.find('div',class_='v-desc').string                   #视频描述
                    AVInfo['id'] = video.find('a',class_='v-author')['href'].split('/')[-1]     #用户id
                    print(AVInfo)
                    exInfo = self.parseAV(video.find('a',class_='title')['href'])
                    exit()


    def parseAV(self,avNum):
        url = biliUrl + avNum
        content = self.getUrl(url)
        # print(content.find('div',class_='v-title-info'))
        aid = re.match(pattern,avNum)
        print(aid)
        url = "http://api.bilibili.com/archive_stat/stat?callback=jQuery1720020664264156293077_1474269696982&aid=6315006&type=jsonp&_=1474269697807"



start = '2016-08-01'
end = '2016-08-31'
spider = BilibiliSpider('game',start, end)
print("分析周期：`{start}` ~ `{end}`".format(start=start,end=end))
spider.start()

