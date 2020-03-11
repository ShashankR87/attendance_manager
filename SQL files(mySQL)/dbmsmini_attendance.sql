CREATE DATABASE  IF NOT EXISTS `dbmsmini` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbmsmini`;
-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: dbmsmini
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `datetaken` date NOT NULL,
  `hour` int(11) NOT NULL,
  `usn` varchar(10) NOT NULL,
  `subjectcode` varchar(10) NOT NULL,
  `sec` varchar(1) DEFAULT NULL,
  `status` varchar(1) NOT NULL DEFAULT 'a',
  PRIMARY KEY (`datetaken`,`hour`,`usn`,`subjectcode`),
  KEY `usn` (`usn`),
  KEY `subjectcode` (`subjectcode`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`usn`) REFERENCES `student` (`usn`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`subjectcode`) REFERENCES `subject` (`subjectcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('2019-11-14',2,'1rn17cs001','17cs01','a','a'),('2019-11-14',2,'1rn17cs003','17cs01','a','p'),('2019-11-14',4,'1rn17cs001','17cs02','a','p'),('2019-11-15',3,'1rn17cs001','17cs01','a','p'),('2019-11-15',3,'1rn17cs002','17cs01','a','p'),('2019-11-15',3,'1rn17cs003','17cs01','a','p'),('2019-11-15',4,'1rn17cs002','17cs01','a','p'),('2019-11-15',4,'1rn17cs003','17cs01','a','p'),('2019-11-23',1,'1rn17cs001','17cs01','a','p'),('2019-11-23',1,'1rn17cs002','17cs01','a','a'),('2019-11-23',1,'1rn17cs003','17cs01','a','p'),('2019-11-23',2,'1rn17cs003','17cs02','a','a'),('2019-11-28',1,'1rn17cs001','17cs01','a','p'),('2019-11-28',1,'1rn17cs002','17cs01','a','a'),('2019-11-28',1,'1rn17cs003','17cs01','a','p'),('2019-11-28',6,'1rn17cs001','17cs01','a','p'),('2019-11-28',6,'1rn17cs002','17cs01','a','p'),('2019-11-28',6,'1rn17cs003','17cs01','a','a');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-29 11:27:40
