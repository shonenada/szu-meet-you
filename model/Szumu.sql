-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- 主机: 127.2.167.1:3306
-- 生成日期: 2013 年 02 月 05 日 09:49
-- 服务器版本: 5.1.67
-- PHP 版本: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `Szumu`
--

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_articles`
--

CREATE TABLE IF NOT EXISTS `szu_mu_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `content` text COLLATE utf8_unicode_ci NOT NULL,
  `author` int(11) NOT NULL,
  `shopid` int(11) NOT NULL,
  `special` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_building`
--

CREATE TABLE IF NOT EXISTS `szu_mu_building` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `ownerid` int(11) NOT NULL DEFAULT '0',
  `mapid` int(11) NOT NULL,
  `mapsite` int(11) NOT NULL,
  `pic` varchar(250) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'nopic.jpg',
  `color` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'brown',
  `descr` text COLLATE utf8_unicode_ci NOT NULL,
  `special` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=13 ;

--
-- 转存表中的数据 `szu_mu_building`
--

INSERT INTO `szu_mu_building` (`id`, `title`, `ownerid`, `mapid`, `mapsite`, `pic`, `color`, `descr`, `special`, `created`) VALUES
(11, '阿达', 12, 25, 0, 'nopic.jpg', 'brown', 'test123', 'shop/private', '0000-00-00 00:00:00'),
(12, '二号店', 0, 25, 2, 'nopic.jpg', 'brown', '', 'rent', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_building-backup`
--

CREATE TABLE IF NOT EXISTS `szu_mu_building-backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `ownerid` int(11) NOT NULL DEFAULT '0',
  `mapid` int(11) NOT NULL,
  `mapsite` int(11) NOT NULL,
  `pic` varchar(250) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'nopic.jpg',
  `color` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'brown',
  `descr` text COLLATE utf8_unicode_ci NOT NULL,
  `special` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=13 ;

--
-- 转存表中的数据 `szu_mu_building-backup`
--

INSERT INTO `szu_mu_building-backup` (`id`, `title`, `ownerid`, `mapid`, `mapsite`, `pic`, `color`, `descr`, `special`, `created`) VALUES
(1, '办公楼', 0, 2, 3, 'nopic.jpg', 'brown', '深大觅友社区办公楼，处理社区各类事务', 'office', '0000-00-00 00:00:00'),
(2, '图书馆北馆', 0, 3, 12, 'nopic.jpg', 'brown', '记载深大觅友社区的点滴历史', 'northlib', '0000-00-00 00:00:00'),
(3, '图书馆南馆', 0, 4, 1, 'nopic.jpg', 'brown', '闻书香，识友人', 'southlib', '0000-00-00 00:00:00'),
(4, '教学楼', 0, 5, 1, 'nopic.jpg', 'brown', '教学楼', 'teach', '0000-00-00 00:00:00'),
(5, '科技楼', 0, 6, 6, 'nopic.jpg', 'brown', '深大觅友社区的实验室', 'tech', '0000-00-00 00:00:00'),
(6, '文科楼', 0, 7, 10, 'nopic.jpg', 'brown', '传承深大文化', 'litera', '0000-00-00 00:00:00'),
(7, '学生活动中心', 0, 8, 3, 'nopic.jpg', 'brown', '学生活动中心，提供各社团信息', 'studentcenter', '0000-00-00 00:00:00'),
(8, '石头坞', 0, 24, 12, 'nopic.jpg', 'brown', '石头坞，昔日的乐园', 'stone', '0000-00-00 00:00:00'),
(9, '元平体育场', 0, 13, 1, 'nopic.jpg', 'brown', '运动造就人脉', 'gym', '0000-00-00 00:00:00'),
(10, '学生宿舍区', 0, 19, 7, 'nopic.jpg', 'brown', '学生宿舍区', 'dorm', '0000-00-00 00:00:00'),
(11, '一号店', 0, 25, 0, 'nopic.jpg', 'brown', '1号店出租中', 'rent', '0000-00-00 00:00:00'),
(12, '二号店', 0, 25, 2, 'nopic.jpg', 'brown', '二号店出租中', 'rent', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_class_comment`
--

CREATE TABLE IF NOT EXISTS `szu_mu_class_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classid` bigint(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `comment` text COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_course`
--

CREATE TABLE IF NOT EXISTS `szu_mu_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` bigint(11) NOT NULL,
  `classname` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `classteacher` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `college` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `mainclass` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `mark` float NOT NULL,
  `checktype` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `ks` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `sjd` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `bz` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `classroom` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_map`
--

CREATE TABLE IF NOT EXISTS `szu_mu_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `descr` text COLLATE utf8_unicode_ci NOT NULL,
  `path` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `link` varchar(47) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0,0,0,0',
  `buildings` text COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=29 ;

--
-- 转存表中的数据 `szu_mu_map`
--

INSERT INTO `szu_mu_map` (`id`, `title`, `descr`, `path`, `link`, `buildings`, `created`) VALUES
(1, 'first map', '深大觅友社区的第一张地图。是一个神秘的地带，进入此地，你将永远出不去。人称“死胡同”', '1,1,1,1', '1,1,1,1', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(2, '办公楼附近', '办公楼附近', '1,1,1,1', '17,18,0,16', 'None,None,None,office,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(3, '图书馆北馆附近', '图书馆北馆附近', '1,1,1,1', '10,20,17,9', 'None,None,None,None,None,None,None,None,None,None,None,None,northlib,None', '0000-00-00 00:00:00'),
(4, '图书馆南馆附近', '图书馆南馆附近', '0,1,1,1', '0,11,10,12', 'None,southlib,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(5, '教学楼附近', '教学楼附近', '1,1,1,1', '21,26,22,11', 'None,teach,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(6, '科技楼附近', '科技楼附近', '1,1,1,0', '14,9,15,0', 'None,None,None,None,None,None,tech,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(7, '文科楼附近', '文科楼附近', '1,1,0,0', '15,16,0,0', 'None,None,None,None,None,None,None,None,None,None,litera,None,None,None', '0000-00-00 00:00:00'),
(8, '学生活动中心附近', '学生活动中心附近', '0,0,1,1', '0,0,24,25', 'None,None,None,student,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(9, '小路', '北馆与科技楼之间的小路', '0,1,0,1', '0,3,0,6', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(10, '小路', '南馆与北馆之间小路', '1,0,1,0', '4,0,3,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(11, '小路', '南馆与教学楼之间小路', '0,1,0,1', '0,5,0,4', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(12, '小路', '南馆与元平体育场之间小路', '0,1,0,1', '0,4,0,13', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(13, '元平体育场附近', '元平体育场附近', '0,1,1,0', '0,12,14,0', 'None,gym,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(14, '小路', '元平体育场与科技楼之间的小路', '1,0,1,0', '13,0,6,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(15, '小路', '科技楼与文科楼之间的小路', '1,0,1,0', '6,0,7,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(16, '小路', '文科楼与办公楼之间的小路', '0,1,0,1', '0,2,0,7', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(17, '小路', '办公楼与北馆之间的小路', '1,0,1,0', '3,0,2,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(18, '小路', '办公楼与学生宿舍区之间的小路', '0,1,0,1', '0,27,0,2', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(19, '学生宿舍区', '学生宿舍区', '1,0,1,1', '22,0,23,20', 'None,None,None,None,None,None,None,dorm,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(20, '小路', '北馆到学生宿舍区之间的小路', '0,1,0,1', '0,19,0,3', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(21, '小路', '教学楼与学生活动中心之间的小路', '1,0,1,0', '28,0,5,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(22, '小路', '学生宿舍区与教学楼之间的小路', '1,0,1,0', '5,0,19,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(23, '小路', '办公楼与学生宿舍区之间的小路', '1,0,1,0', '19,0,27,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(24, '石头坞附近', '石头坞附近', '1,0,0,1', '8,0,0,26', 'None,None,None,None,None,None,None,None,None,None,None,None,stone,None', '0000-00-00 00:00:00'),
(25, '小路', '教学楼与学生活动中心之间的小路', '0,1,0,1', '0,8,0,28', '11,None,12,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(26, '小路', '教学楼与石头坞之间的小路', '0,1,0,1', '0,24,0,5', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(27, '拐角', '办公楼到学生宿舍区之间的拐角', '1,0,0,1', '23,0,0,18', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00'),
(28, '拐角', '教学楼与学生活动中心之间的拐角', '0,1,1,0', '0,25,21,0', 'None,None,None,None,None,None,None,None,None,None,None,None,None,None', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_msg`
--

CREATE TABLE IF NOT EXISTS `szu_mu_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fromid` int(11) NOT NULL,
  `toid` int(11) NOT NULL,
  `msg` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  `from_hide` int(1) NOT NULL DEFAULT '0',
  `to_hide` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_relationship`
--

CREATE TABLE IF NOT EXISTS `szu_mu_relationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fromid` int(11) NOT NULL,
  `toid` int(11) NOT NULL,
  `relationship` tinyint(1) NOT NULL DEFAULT '1',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_stuselect`
--

CREATE TABLE IF NOT EXISTS `szu_mu_stuselect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` bigint(11) NOT NULL,
  `truename` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `gender` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `major` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `cid` bigint(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `szu_mu_user`
--

CREATE TABLE IF NOT EXISTS `szu_mu_user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(70) CHARACTER SET utf8 NOT NULL,
  `password` varchar(32) CHARACTER SET utf8 NOT NULL,
  `token` varchar(32) CHARACTER SET utf8 NOT NULL,
  `nickname` varchar(20) CHARACTER SET utf8 NOT NULL,
  `number` int(15) DEFAULT NULL,
  `truename` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `birthday` date NOT NULL,
  `college` int(2) DEFAULT NULL,
  `phone` bigint(11) DEFAULT NULL,
  `shortPhone` int(6) DEFAULT NULL,
  `qq` bigint(15) DEFAULT NULL,
  `money` decimal(10,0) NOT NULL DEFAULT '0',
  `mark` float NOT NULL DEFAULT '0',
  `regTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `regIP` varchar(40) CHARACTER SET utf8 NOT NULL,
  `logTime` datetime DEFAULT NULL,
  `logIP` varchar(40) CHARACTER SET utf8 DEFAULT NULL,
  `state` tinyint(1) DEFAULT '1',
  `trash` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=17 ;

--
-- 转存表中的数据 `szu_mu_user`
--

INSERT INTO `szu_mu_user` (`id`, `username`, `password`, `token`, `nickname`, `number`, `truename`, `gender`, `birthday`, `college`, `phone`, `shortPhone`, `qq`, `money`, `mark`, `regTime`, `regIP`, `logTime`, `logIP`, `state`, `trash`) VALUES
(12, 'shonenada@gmail.com', 'e8c847beddb733199421ce4661bf2c08', '03e86f477271344e3943c7dedd3e76e5', '阿达', 2011150337, '刘耀达', 1, '1992-11-22', 14, 13424251220, 681220, 181011678, '0', 0, '2012-08-15 16:00:03', '192.168.1.101', '2012-12-02 18:06:03', '172.31.196.31', 3, 0),
(13, '181011678@qq.com', 'e8c847beddb733199421ce4661bf2c08', '88fe457abf50220454556748ebda9652', '达达', 2011150005, '邱宇轩', 0, '1992-11-22', 14, 0, 0, 0, '0', 0, '2012-08-16 05:22:16', '192.168.1.101', '2012-10-28 08:08:15', '172.31.196.21', 1, 0),
(16, 'szumeetu@gmail.com', '7570d19a7322a48d05cb4b5e94fe612d', ' ', '深大觅友社区', 2011150210, '罗志浩', 1, '0000-00-00', NULL, NULL, NULL, NULL, '0', 0, '2012-08-23 12:45:53', '172.31.196.21', NULL, NULL, 1, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
