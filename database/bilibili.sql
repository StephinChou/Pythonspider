/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2016-09-20 15:20:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `bilibili`
-- ----------------------------
DROP TABLE IF EXISTS `bilibili`;
CREATE TABLE `bilibili` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `av` varchar(10) NOT NULL COMMENT '视频av号',
  `title` varchar(100) NOT NULL COMMENT '视频标题',
  `module` varchar(20) NOT NULL DEFAULT '' COMMENT '视频模块',
  `tid` varchar(5) NOT NULL DEFAULT '' COMMENT '模块编号',
  `author` varchar(10) NOT NULL COMMENT '作者id',
  `author_name` varchar(30) NOT NULL COMMENT '作者名字',
  `play` int(11) NOT NULL COMMENT '播放数',
  `danmu` int(11) NOT NULL COMMENT '弹幕数',
  `collect` int(11) NOT NULL COMMENT '收藏数',
  `desc` varchar(500) NOT NULL COMMENT '视频描述',
  `share` int(11) NOT NULL COMMENT '分享数',
  `coin` int(11) NOT NULL COMMENT '硬币数',
  `mtime` int(11) NOT NULL COMMENT '修改时间',
  `ctime` int(11) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UQ_video` (`av`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=436 DEFAULT CHARSET=utf8mb4;
