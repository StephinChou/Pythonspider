# 爬取B站 视频热度排行的 视频数据  bilibili.py
* 只需输入一个大模块名，如游戏模块名为'game'，自行会爬取下面几个小类，并按播放数、硬币数等排行分别爬取
* 已解析出数据接口，直接获取视频数据，不使用webDriver，爬取速度提升数十倍,并且不会miss数据2016.9.22 
* @TODO 对爬取到的视频做日期归类（待完成）
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
 
 ![](https://github.com/StephinChou/Pythonspider/blob/master/image/1.png)
