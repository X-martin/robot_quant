/*
Navicat MySQL Data Transfer

Source Server         : zabbix
Source Server Version : 50717
Source Host           : 192.168.2.31:3306
Source Database       : strategy

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-06-20 17:28:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for r_order
-- ----------------------------
DROP TABLE IF EXISTS `r_order`;
CREATE TABLE `r_order` (
  `strategy_id` int(8) NOT NULL,
  `stockcode` varchar(9) NOT NULL,
  `tradedate` date NOT NULL,
  `money` decimal(32,16) DEFAULT NULL,
  `num` decimal(8,0) DEFAULT NULL,
  PRIMARY KEY (`strategy_id`,`stockcode`,`tradedate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for r_position
-- ----------------------------
DROP TABLE IF EXISTS `r_position`;
CREATE TABLE `r_position` (
  `strategy_id` int(8) NOT NULL,
  `stockcode` varchar(9) NOT NULL,
  `tradedate` date NOT NULL,
  `money` decimal(32,16) DEFAULT NULL,
  `num` decimal(8,0) DEFAULT NULL,
  PRIMARY KEY (`strategy_id`,`tradedate`,`stockcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for r_strategy
-- ----------------------------
DROP TABLE IF EXISTS `r_strategy`;
CREATE TABLE `r_strategy` (
  `strategy_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`strategy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for sys_tradeday
-- ----------------------------
DROP TABLE IF EXISTS `sys_tradeday`;
CREATE TABLE `sys_tradeday` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tradedate` date NOT NULL,
  `type` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8352 DEFAULT CHARSET=utf8;
