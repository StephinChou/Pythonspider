# Pythonspider,一个简单的python爬虫
* 娱乐随手写的，代码不太严谨，仅仅实现功能
* 原生python+BeautifulSoup4
* python3.4版本
* 所有脚本要和spider.py放到同一目录下
* 自行下载BeautifulSoup4 的类库

## 爬取知乎的爬虫 zhihu.py 
* 主要实现 爬取一个收藏夹 里 所有问题答案下的 图片(你懂得)
* 文字信息暂未收录，可自行实现，比图片更简单
* 具体代码里有详细注释，请自行阅读

## 爬取B站 视频热度排行的 视频数据  bilibili.py
* 只需输入一个大模块名，如游戏模块名为'game'，自行会爬取下面几个小类，并按播放数、硬币数等排行分别爬取
* 因为B站的数据由js获取，并且逻辑较为复杂，视频详细页的数据由 selenium模块来实现，效率不高，并且会miss
* 关于selenium的信息，请谷歌"selenium python",这是我翻译的 [selenium + python 的文档](https://github.com/StephinChou/seleniumDocument)
* 目前爬取的信息有：
 * up主id
 * up主名
 * 视频AV号
 * 播放数
 * 收藏数
 * 弹幕数
 * 视频描述
 * 硬币数(获取不稳定，少数会获取不到)
 * 分享数(同上)





### 有一个sis的爬虫，可以下种子和图片，不过普通网络不太稳定，不好测试，暂时不传上来
