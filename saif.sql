-- MySQL dump 10.13  Distrib 5.7.16, for Win64 (x86_64)
--
-- Host: localhost    Database: saif
-- ------------------------------------------------------
-- Server version	5.7.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `symbol` char(6) CHARACTER SET latin1 NOT NULL,
  `year` char(4) CHARACTER SET latin1 NOT NULL,
  `article` longtext,
  `reportcol` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `avgwords` float DEFAULT NULL,
  `sentences` int(11) DEFAULT NULL,
  `words` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `process_step` int(11) DEFAULT NULL,
  PRIMARY KEY (`symbol`,`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wordstatistic`
--

DROP TABLE IF EXISTS `wordstatistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wordstatistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` char(128) NOT NULL,
  `cha1` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `cha2` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `cha3` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `cha4` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `cha5` char(10) CHARACTER SET latin1 DEFAULT NULL,
  `symbol` char(6) CHARACTER SET latin1 NOT NULL,
  `year` int(11) NOT NULL,
  `amt` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`word`,`symbol`,`year`)
) ENGINE=InnoDB AUTO_INCREMENT=4767 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-21 11:35:10
