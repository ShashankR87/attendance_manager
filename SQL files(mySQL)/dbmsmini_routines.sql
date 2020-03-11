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
-- Temporary view structure for view `ptab`
--

DROP TABLE IF EXISTS `ptab`;
/*!50001 DROP VIEW IF EXISTS `ptab`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `ptab` AS SELECT 
 1 AS `day`,
 1 AS `hour`,
 1 AS `count(*)`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `atab`
--

DROP TABLE IF EXISTS `atab`;
/*!50001 DROP VIEW IF EXISTS `atab`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `atab` AS SELECT 
 1 AS `day`,
 1 AS `hour`,
 1 AS `count(*)`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `ptab`
--

/*!50001 DROP VIEW IF EXISTS `ptab`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`shreyas`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ptab` AS select dayofmonth(`attendance`.`datetaken`) AS `day`,`attendance`.`hour` AS `hour`,count(0) AS `count(*)` from `attendance` where ((month(`attendance`.`datetaken`) = '11') and (`attendance`.`subjectcode` = '17cs01') and (`attendance`.`sec` = 'a') and (`attendance`.`status` = 'p')) group by `attendance`.`datetaken`,`attendance`.`hour` order by `attendance`.`datetaken`,`attendance`.`hour` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `atab`
--

/*!50001 DROP VIEW IF EXISTS `atab`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`shreyas`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `atab` AS select dayofmonth(`attendance`.`datetaken`) AS `day`,`attendance`.`hour` AS `hour`,count(0) AS `count(*)` from `attendance` where ((month(`attendance`.`datetaken`) = '11') and (`attendance`.`subjectcode` = '17cs01') and (`attendance`.`sec` = 'a') and (`attendance`.`status` = 'a')) group by `attendance`.`datetaken`,`attendance`.`hour` order by `attendance`.`datetaken`,`attendance`.`hour` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Dumping events for database 'dbmsmini'
--

--
-- Dumping routines for database 'dbmsmini'
--
/*!50003 DROP PROCEDURE IF EXISTS `fillTeaches` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`shreyas`@`%` PROCEDURE `fillTeaches`()
begin
declare stid varchar(10);
declare us varchar(10);
declare sub varchar(10);
declare staffcur cursor for select A.staffid from taughtby A, student S, subject U where  U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec and A.elective='N';
declare uscur cursor for select S.usn from taughtby A, student S, subject U where U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec and A.elective='N';
declare subcur cursor for select U.subjectcode from taughtby A, student S, subject U where U.sem=S.sem and U.subjectcode=A.subjectcode and A.sec=S.sec and A.elective='N';
open staffcur;
open uscur;
open subcur;
drop table teaches;
create table teaches(
    staffid varchar(10),
    usn varchar(10),
    subjectcode varchar(10),
    primary key(staffid,usn,subjectcode),
   foreign key (staffid) references teacher(staffid),
   foreign key (usn) references student(usn),
  foreign key (subjectcode) references subject(subjectcode)
);
filltable: loop
fetch staffcur into stid;
fetch uscur into us;
fetch subcur into sub;
insert into teaches values (stid, us, sub);
commit;
end loop filltable;
close staffcur;
close uscur;
close subcur;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-29 11:27:44
