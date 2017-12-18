/*
Navicat MySQL Data Transfer

Source Server         : ali-47.104
Source Server Version : 50717
Source Host           : 47.104.97.149:3306
Source Database       : robot_quant

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-12-18 16:57:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for demo
-- ----------------------------
DROP TABLE IF EXISTS `demo`;
CREATE TABLE `demo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for r_order
-- ----------------------------
DROP TABLE IF EXISTS `r_order`;
CREATE TABLE `r_order` (
  `strategy_id` int(8) NOT NULL,
  `stockcode` varchar(9) NOT NULL,
  `tradedate` datetime NOT NULL,
  `price` decimal(32,16) DEFAULT NULL,
  `volume` decimal(8,0) DEFAULT NULL,
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
  `current_price` decimal(32,16) DEFAULT NULL,
  `price` decimal(32,16) DEFAULT NULL,
  `volume` decimal(8,0) DEFAULT NULL,
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
-- Table structure for ST_FACTOR
-- ----------------------------
DROP TABLE IF EXISTS `ST_FACTOR`;
CREATE TABLE `ST_FACTOR` (
  `FACTOR_ID` int(11) NOT NULL,
  `FACTOR_NAME` varchar(64) NOT NULL,
  `FACTOR_ENNAME` varchar(32) DEFAULT NULL,
  `TYPE` smallint(6) DEFAULT NULL,
  `CREATE_DATE` datetime NOT NULL,
  `UPDATE_DATE` datetime DEFAULT NULL,
  `TRACETYPE` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`FACTOR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ST_FACTOR_VALUE
-- ----------------------------
DROP TABLE IF EXISTS `ST_FACTOR_VALUE`;
CREATE TABLE `ST_FACTOR_VALUE` (
  `FACTOR_VALUE_ID` varchar(32) NOT NULL,
  `FACTOR_ID` int(11) NOT NULL,
  `STOCKCODE` varchar(9) NOT NULL,
  `FACTOR_DATE` datetime NOT NULL,
  `FACTOR_VALUE` varchar(128) NOT NULL,
  `CREATE_TIME` datetime DEFAULT NULL,
  `UPDATE_TIME` datetime DEFAULT NULL,
  `REPORT_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`FACTOR_VALUE_ID`),
  KEY `FACTOR_DATE_IDX` (`FACTOR_DATE`) USING BTREE,
  KEY `FACTOR_ID_IDX` (`FACTOR_ID`) USING BTREE,
  KEY `STOCKCODE_IDX` (`STOCKCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ST_INDEXTRADE_DATA
-- ----------------------------
DROP TABLE IF EXISTS `ST_INDEXTRADE_DATA`;
CREATE TABLE `ST_INDEXTRADE_DATA` (
  `INDEXCODE` varchar(9) NOT NULL COMMENT '指数代码',
  `TRADEDATE` datetime NOT NULL COMMENT '日期',
  `PRE_CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '前收盘价',
  `OPENPRICE` decimal(32,16) DEFAULT NULL COMMENT '开盘价',
  `HIGHPRICE` decimal(32,16) DEFAULT NULL COMMENT '最高价',
  `LOWPRICE` decimal(32,16) DEFAULT NULL COMMENT '最低价',
  `CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '收盘价',
  `VOLUME` decimal(16,0) DEFAULT NULL COMMENT '成交量',
  `AMT` decimal(32,16) DEFAULT NULL COMMENT '成交额',
  `CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌',
  `PCT_CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌幅',
  `SWING` decimal(32,16) DEFAULT NULL COMMENT '振幅',
  `VWAP` decimal(32,16) DEFAULT NULL COMMENT '均价',
  `CREATE_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`INDEXCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_ST_INDEXTRADE_DATA_UNQ` (`TRADEDATE`,`INDEXCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='指数交易数据';

-- ----------------------------
-- Table structure for ST_INDEXTRADE_DATA_M
-- ----------------------------
DROP TABLE IF EXISTS `ST_INDEXTRADE_DATA_M`;
CREATE TABLE `ST_INDEXTRADE_DATA_M` (
  `INDEXCODE` varchar(9) NOT NULL COMMENT '指数代码',
  `TRADEDATE` datetime NOT NULL COMMENT '日期',
  `PRE_CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '前收盘价',
  `OPENPRICE` decimal(32,16) DEFAULT NULL COMMENT '开盘价',
  `HIGHPRICE` decimal(32,16) DEFAULT NULL COMMENT '最高价',
  `LOWPRICE` decimal(32,16) DEFAULT NULL COMMENT '最低价',
  `CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '收盘价',
  `VOLUME` decimal(16,0) DEFAULT NULL COMMENT '成交量',
  `AMT` decimal(32,16) DEFAULT NULL COMMENT '成交额',
  `CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌',
  `PCT_CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌幅',
  `SWING` decimal(32,16) DEFAULT NULL COMMENT '振幅',
  `VWAP` decimal(32,16) DEFAULT NULL COMMENT '均价',
  `CREATE_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`INDEXCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_ST_INDEXTRADE_DATA_M_UNQ` (`TRADEDATE`,`INDEXCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='指数交易数据-月';

-- ----------------------------
-- Table structure for ST_INDEXTRADE_DATA_W
-- ----------------------------
DROP TABLE IF EXISTS `ST_INDEXTRADE_DATA_W`;
CREATE TABLE `ST_INDEXTRADE_DATA_W` (
  `INDEXCODE` varchar(9) NOT NULL COMMENT '指数代码',
  `TRADEDATE` datetime NOT NULL COMMENT '日期',
  `PRE_CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '前收盘价',
  `OPENPRICE` decimal(32,16) DEFAULT NULL COMMENT '开盘价',
  `HIGHPRICE` decimal(32,16) DEFAULT NULL COMMENT '最高价',
  `LOWPRICE` decimal(32,16) DEFAULT NULL COMMENT '最低价',
  `CLOSEPRICE` decimal(32,16) DEFAULT NULL COMMENT '收盘价',
  `VOLUME` decimal(16,0) DEFAULT NULL COMMENT '成交量',
  `AMT` decimal(32,16) DEFAULT NULL COMMENT '成交额',
  `CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌',
  `PCT_CHG` decimal(32,16) DEFAULT NULL COMMENT '涨跌幅',
  `SWING` decimal(32,16) DEFAULT NULL COMMENT '振幅',
  `VWAP` decimal(32,16) DEFAULT NULL COMMENT '均价',
  `CREATE_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`INDEXCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_ST_INDEXTRADE_DATA_W_UNQ` (`TRADEDATE`,`INDEXCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='指数交易数据-周';

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

-- ----------------------------
-- Table structure for W_CONSTITUTE_300
-- ----------------------------
DROP TABLE IF EXISTS `W_CONSTITUTE_300`;
CREATE TABLE `W_CONSTITUTE_300` (
  `TRADEDATE` datetime NOT NULL,
  `STOCKCODE` varchar(9) NOT NULL,
  `STOCKNAME` varchar(16) DEFAULT NULL,
  `WEIGHT` decimal(8,4) DEFAULT NULL COMMENT '权重',
  PRIMARY KEY (`STOCKCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_W_CONSTITUTE_300_UNQ` (`TRADEDATE`,`STOCKCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='万得300成分股表';

-- ----------------------------
-- Table structure for W_CONSTITUTE_50
-- ----------------------------
DROP TABLE IF EXISTS `W_CONSTITUTE_50`;
CREATE TABLE `W_CONSTITUTE_50` (
  `TRADEDATE` datetime NOT NULL,
  `STOCKCODE` varchar(9) NOT NULL,
  `STOCKNAME` varchar(16) DEFAULT NULL,
  `WEIGHT` decimal(8,4) DEFAULT NULL COMMENT '权重',
  PRIMARY KEY (`STOCKCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_W_CONSTITUTE_50_UNQ` (`TRADEDATE`,`STOCKCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='万得50成分股表';

-- ----------------------------
-- Table structure for W_CONSTITUTE_500
-- ----------------------------
DROP TABLE IF EXISTS `W_CONSTITUTE_500`;
CREATE TABLE `W_CONSTITUTE_500` (
  `TRADEDATE` datetime NOT NULL,
  `STOCKCODE` varchar(9) NOT NULL,
  `STOCKNAME` varchar(16) DEFAULT NULL,
  `WEIGHT` decimal(8,4) DEFAULT NULL COMMENT '权重',
  PRIMARY KEY (`STOCKCODE`,`TRADEDATE`),
  UNIQUE KEY `IDX_W_CONSTITUTE_500_UNQ` (`TRADEDATE`,`STOCKCODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='万得500成分股表';
