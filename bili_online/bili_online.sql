/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2016-09-21 15:14:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `bili_online`
-- ----------------------------
DROP TABLE IF EXISTS `bili_online`;
CREATE TABLE `bili_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `online` int(11) NOT NULL COMMENT '在线人数',
  `ctime` int(11) NOT NULL DEFAULT '0' COMMENT '时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ctime` (`ctime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

