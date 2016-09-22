#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-20 15:42:13
# @Author  : waitingChou (zhouzt52@qq.com)
# @Link    : https://github.com/StephinChou/
__author__ = 'waiting'
from spider import SpiderHTML
from multiprocessing import Pool
import sys,urllib,http,os,re,time,codecs,json
import pymysql
pymysql.install_as_MySQLdb()

#从本地记录里获取曾经爬取过的视频号
f = open('avSet.txt','r')
avSet = set([])
for line in f:
    avSet = set(line.split(','))

#一些配置
conn = pymysql.connect(host='localhost',user='root',passwd='',db='test',port=3306,use_unicode=True, charset="utf8")
cur=conn.cursor()
pattern = re.compile(r'\d+')    #获取av号的正则表达式
orders = {"hot":"播放量","review":"评论数","promote":"硬币数","stow":"收藏数"}
biliUrl = 'http://www.bilibili.com'

class BilibiliSpider(SpiderHTML):
    def __init__(self,module,timeStart,timeEnd,limit):
        self.url = biliUrl + '/video/' + module + '.html'
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.limit = limit

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
            print("对子模块‘{typeName}’进行‘{name}’排序的分析".format(name=name,typeName=typeName))
            sort = 0;
            #是否获取到足够的排名
            isBreak = False
            for page in range(1,5):
                # http://www.bilibili.com/list/stow-65-1-2016-09-12~2016-09-19.html
                urlTmp = biliUrl + "/list/{order}-{tid}-{page}-{start}~{end}.html".format(order=order,tid=tid,page=page,start=self.timeStart,end=self.timeEnd)
                content = self.getUrl(urlTmp)

                videoContent = content.find('ul',class_='vd-list l1')
                videoList = videoContent.find_all('div',class_='l-item')
                
                for video in videoList:
                    AVInfo = dict()     #作品信息
                    AVInfo['av'] = pattern.search(video.find('a',class_='title')['href']).group()   #av号
                    AVInfo['title'] = video.find('a',class_='title').string                     #标题
                    sort=sort+1
                    if AVInfo['av'] in avSet:
                        print("已经爬取过该视频av{av},{title}".format(**AVInfo))
                        continue
                    
                    AVInfo['author_name'] = video.find('a',class_='v-author').string            #作者
                    AVInfo['module'] = typeName                                                 #模块名
                    AVInfo['tid'] = tid                                                         #模块id
                    coinInfo = self.parseAV(AVInfo['av'])             #解析详细视频页面获取硬币和收藏数
                    if coinInfo == 0:
                        sort=sort-1
                        print("作品名：{title},【视频信息获取失败】".format(**AVInfo))
                        continue

                    AVInfo['play'] = video.find('span',class_='v-info-i gk').span.string        #播放数
                    AVInfo['danmu'] = video.find('span',class_='v-info-i dm').span.string       #弹幕数
                    AVInfo['collect'] = video.find('span',class_='v-info-i sc').span.string     #收藏数
                    AVInfo['url'] = biliUrl + video.find('a',class_='title')['href']            #视频链接
                    AVInfo['desc'] = video.find('div',class_='v-desc').string                   #视频描述
                    AVInfo['author'] = video.find('a',class_='v-author')['href'].split('/')[-1]     #用户id
                    #将此视频加入已经爬取过的列表
                    avSet.add(AVInfo['av'])
                    AVInfo['mtime'] = int(time.time())
                    AVInfo['ctime'] = int(time.time())
                    #合并信息
                    AVInfo = dict(coinInfo,**AVInfo)

                    print("排名第{sort}：\t{author_name},\t播放量:{play},\t收藏数:{collect},\t硬币数:{coin},\t作品名：{title}".format(sort=sort,**AVInfo))
                    sql = "INSERT IGNORE INTO `bilibili`(`av`, `title`, `module`,`tid`,`author`, `author_name`, `play`, `danmu`, `collect`, `desc`, `share`, `coin`, `mtime`, `ctime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    args = (AVInfo['av'],AVInfo['title'],AVInfo['module'],AVInfo['tid'],AVInfo['author'],AVInfo['author_name'],AVInfo['play'],AVInfo['danmu'],AVInfo['collect'],AVInfo['desc'],AVInfo['share'],AVInfo['coin'],AVInfo['mtime'],AVInfo['ctime'])
                    cur.execute(sql,args)
                    conn.commit()
                    if sort >= self.limit:
                        isBreak = True
                        break
                if isBreak == True:
                    break
        #全部获取完毕，保存av号
        with codecs.open('avSet.txt', encoding='utf-8', mode='w') as f:
            f.write(','.join(str(s) for s in avSet))
                    

    #解析单独的一个视频
    # @param avNum String video/av6315006/
    def parseAV(self,avNum):
        url = "http://api.bilibili.com/archive_stat/stat?callback=&aid={av}&type=jsonp&_={time}".format(av=avNum,time=int(time.time()*1000))
        info = dict()

        try:
            content = self.getUrl(url)
            data = json.loads(str(content))
            info['coin'] = data['data']['coin']
            info['share'] = data['data']['share']
        except:
            return 0;
        return info

#module 为 分类 :游戏 game 舞蹈 dance等
module = 'game'
#热度统计开始时间
start = '2016-07-01'
#热度统计结束时间
end = '2016-07-31'
#单个模块排名获取个数100以内
limit = 40
spider = BilibiliSpider(module,start, end,limit)
print("分析周期：`{start}` ~ `{end}`".format(start=start,end=end))
spider.start()

