-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: phytovault
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `plant_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`),
  KEY `user_id` (`user_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `subject` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicinal_uses`
--

DROP TABLE IF EXISTS `medicinal_uses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicinal_uses` (
  `use_id` int NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`use_id`),
  KEY `idx_disease` (`disease_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicinal_uses`
--

LOCK TABLES `medicinal_uses` WRITE;
/*!40000 ALTER TABLE `medicinal_uses` DISABLE KEYS */;
INSERT INTO `medicinal_uses` VALUES (1,'Wound Healing',NULL),(2,'Cough and Fever',NULL),(3,'Treat Wounds',NULL),(4,'Infections',NULL);
/*!40000 ALTER TABLE `medicinal_uses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_phytochemicals`
--

DROP TABLE IF EXISTS `paper_phytochemicals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paper_phytochemicals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paper_id` int NOT NULL,
  `phytochemical_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paper_id` (`paper_id`),
  KEY `phytochemical_id` (`phytochemical_id`),
  CONSTRAINT `paper_phytochemicals_ibfk_1` FOREIGN KEY (`paper_id`) REFERENCES `research_papers` (`paper_id`) ON DELETE CASCADE,
  CONSTRAINT `paper_phytochemicals_ibfk_2` FOREIGN KEY (`phytochemical_id`) REFERENCES `phytochemicals` (`phytochemical_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_phytochemicals`
--

LOCK TABLES `paper_phytochemicals` WRITE;
/*!40000 ALTER TABLE `paper_phytochemicals` DISABLE KEYS */;
/*!40000 ALTER TABLE `paper_phytochemicals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_plants`
--

DROP TABLE IF EXISTS `paper_plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paper_plants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paper_id` int NOT NULL,
  `plant_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paper_id` (`paper_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `paper_plants_ibfk_1` FOREIGN KEY (`paper_id`) REFERENCES `research_papers` (`paper_id`) ON DELETE CASCADE,
  CONSTRAINT `paper_plants_ibfk_2` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_plants`
--

LOCK TABLES `paper_plants` WRITE;
/*!40000 ALTER TABLE `paper_plants` DISABLE KEYS */;
/*!40000 ALTER TABLE `paper_plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_resets`
--

DROP TABLE IF EXISTS `password_resets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_resets` (
  `reset_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `otp_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reset_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_resets`
--

LOCK TABLES `password_resets` WRITE;
/*!40000 ALTER TABLE `password_resets` DISABLE KEYS */;
INSERT INTO `password_resets` VALUES (1,2,'$2b$12$zYml5Vjhgm3kyCojdbfX9uZSIElhSdslggNHq3eyBGMVUIRY7dIDO','2026-07-10 01:49:02',0,'2026-07-09 20:09:01'),(2,2,'$2b$12$utpnUGInyDn1bCLLz7KJb.cNO3d1MSQqhxEf1FyvoV8fOhDUimQmW','2026-07-10 01:57:02',0,'2026-07-09 20:17:01'),(3,2,'$2b$12$.IyjcdRxTf/Ad3L8oH06wOFZtZiWHlOtzzMgvU.PYxSsaYjSBr.ii','2026-07-10 01:58:30',0,'2026-07-09 20:18:29'),(4,2,'$2b$12$gFMVnvR3dImIPwh/qNmM5u0NumWjAKWeB2x3FVRvjpyUCRe0UFewO','2026-07-10 02:01:35',0,'2026-07-09 20:21:34'),(5,2,'$2b$12$SOAmJhyKP0VJ/38DCE.dBeCI0.kWSe640jR3dW1ylIjrZORK0XUfe','2026-07-10 02:02:43',0,'2026-07-09 20:22:43'),(6,2,'$2b$12$Hcp9Cy0TNK7IWGIddqgTI.1g8VpdV/TOuaXhfyxUIHnSGyt0acunC','2026-07-10 02:06:15',1,'2026-07-09 20:26:14'),(7,2,'$2b$12$FO6cpd9Dg3KYsV5CPsQ4IO6bZiwPDvQjI/o/3jrRxllQ4UE8Wl2Vy','2026-07-10 02:32:34',1,'2026-07-09 20:52:33'),(8,4,'$2b$12$Tm0qjU1TOKeQ4t2hi5MQPOPK/6E3jGfbCKoYMQg0IP08tAxituEti','2026-07-11 23:46:31',1,'2026-07-11 18:06:30');
/*!40000 ALTER TABLE `password_resets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phytochemicals`
--

DROP TABLE IF EXISTS `phytochemicals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phytochemicals` (
  `phytochemical_id` int NOT NULL AUTO_INCREMENT,
  `compound_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `molecular_formula` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `molecular_weight` decimal(10,4) DEFAULT NULL,
  `smiles` text COLLATE utf8mb4_unicode_ci,
  `iupac_name` text COLLATE utf8mb4_unicode_ci,
  `pubchem_cid` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `biological_activity` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`phytochemical_id`),
  KEY `idx_compound_name` (`compound_name`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phytochemicals`
--

LOCK TABLES `phytochemicals` WRITE;
/*!40000 ALTER TABLE `phytochemicals` DISABLE KEYS */;
INSERT INTO `phytochemicals` VALUES (1,'Curcumin','C21H20O6',NULL,NULL,NULL,NULL,'Major bioactive compound of turmeric.',NULL,'2026-07-06 22:09:59'),(2,'Azadirachtin','C35H44O16',NULL,NULL,NULL,NULL,'Bioactive compound found in Neem.',NULL,'2026-07-06 22:09:59'),(3,'Eugenol','C10H12O2',NULL,NULL,NULL,NULL,'Major compound present in Tulsi.',NULL,'2026-07-06 22:09:59'),(4,'Withanolide','C28H38O6',NULL,NULL,NULL,NULL,'Major compound of Ashwagandha.',NULL,'2026-07-06 22:09:59'),(5,'• α-Muurolol (major essential oil component)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(6,'• 2-deoxo-2-(acetyloxy)-9-oxoageraphorone (DAOA)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(7,'• 9-oxoagerophorone (OA)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(8,'• Euptox A',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(9,'• Agerophorone derivatives',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(10,'• Quercetin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(11,'• Kaempferol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 20:55:08'),(12,'• Isorhamnetin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(13,'• Caffeic acid',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(14,'• p-Coumaric acid',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(15,'• Tannins',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(16,'• Saponins',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(17,'• Cardiac glycosides',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(18,'• Quinones',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(19,'• Coumarins',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(20,'• Steroids',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(21,'• Alkaloids',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:18:46'),(22,'• Polyacetylenes (e.g.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(23,'Phenylheptatriyne',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(24,'Cytopiloyne)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(25,'• Flavonoids (e.g.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(26,'Quercetin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(27,'Luteolin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(28,'Okanin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(29,'Rutin',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(30,'Isoookanin)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(31,'• Phenolic Acids (e.g.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(32,'Chlorogenic acid',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(33,'Caffeic acid',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(34,'Gallic acid)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(35,'• Phytosterols & Terpenoids (e.g.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(36,'β-sitosterol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(37,'Stigmasterol',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(38,'Friedelin)',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(39,'• Alkaloids & Saponins',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46'),(40,'• Tannins & Carotenoids',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-10-16 21:48:46');
/*!40000 ALTER TABLE `phytochemicals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plant_images`
--

DROP TABLE IF EXISTS `plant_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int NOT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `caption` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `plant_images_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plant_images`
--

LOCK TABLES `plant_images` WRITE;
/*!40000 ALTER TABLE `plant_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `plant_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plant_parts`
--

DROP TABLE IF EXISTS `plant_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant_parts` (
  `part_id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int NOT NULL,
  `part_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`part_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `plant_parts_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plant_parts`
--

LOCK TABLES `plant_parts` WRITE;
/*!40000 ALTER TABLE `plant_parts` DISABLE KEYS */;
INSERT INTO `plant_parts` VALUES (1,7,'Leaf',NULL),(2,11,'Entire Plant msotly leaves and young shoots',NULL);
/*!40000 ALTER TABLE `plant_parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plant_phytochemicals`
--

DROP TABLE IF EXISTS `plant_phytochemicals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant_phytochemicals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int NOT NULL,
  `phytochemical_id` int NOT NULL,
  `plant_part` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `concentration` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `plant_id` (`plant_id`),
  KEY `phytochemical_id` (`phytochemical_id`),
  CONSTRAINT `plant_phytochemicals_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE,
  CONSTRAINT `plant_phytochemicals_ibfk_2` FOREIGN KEY (`phytochemical_id`) REFERENCES `phytochemicals` (`phytochemical_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plant_phytochemicals`
--

LOCK TABLES `plant_phytochemicals` WRITE;
/*!40000 ALTER TABLE `plant_phytochemicals` DISABLE KEYS */;
INSERT INTO `plant_phytochemicals` VALUES (1,7,5,NULL,NULL,NULL),(2,7,6,NULL,NULL,NULL),(3,7,7,NULL,NULL,NULL),(4,7,8,NULL,NULL,NULL),(5,7,9,NULL,NULL,NULL),(6,7,10,NULL,NULL,NULL),(7,7,11,NULL,NULL,NULL),(8,7,12,NULL,NULL,NULL),(9,7,13,NULL,NULL,NULL),(10,7,14,NULL,NULL,NULL),(11,7,15,NULL,NULL,NULL),(12,7,16,NULL,NULL,NULL),(13,7,17,NULL,NULL,NULL),(14,7,18,NULL,NULL,NULL),(15,7,19,NULL,NULL,NULL),(16,7,20,NULL,NULL,NULL),(17,7,21,NULL,NULL,NULL),(18,11,22,NULL,NULL,NULL),(19,11,23,NULL,NULL,NULL),(20,11,24,NULL,NULL,NULL),(21,11,25,NULL,NULL,NULL),(22,11,26,NULL,NULL,NULL),(23,11,27,NULL,NULL,NULL),(24,11,28,NULL,NULL,NULL),(25,11,29,NULL,NULL,NULL),(26,11,30,NULL,NULL,NULL),(27,11,31,NULL,NULL,NULL),(28,11,32,NULL,NULL,NULL),(29,11,33,NULL,NULL,NULL),(30,11,34,NULL,NULL,NULL),(31,11,35,NULL,NULL,NULL),(32,11,36,NULL,NULL,NULL),(33,11,37,NULL,NULL,NULL),(34,11,38,NULL,NULL,NULL),(35,11,39,NULL,NULL,NULL),(36,11,40,NULL,NULL,NULL);
/*!40000 ALTER TABLE `plant_phytochemicals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plant_uses`
--

DROP TABLE IF EXISTS `plant_uses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant_uses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int NOT NULL,
  `use_id` int NOT NULL,
  `evidence_level` enum('Traditional','Experimental','Clinical') COLLATE utf8mb4_unicode_ci DEFAULT 'Traditional',
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `plant_id` (`plant_id`),
  KEY `use_id` (`use_id`),
  CONSTRAINT `plant_uses_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE,
  CONSTRAINT `plant_uses_ibfk_2` FOREIGN KEY (`use_id`) REFERENCES `medicinal_uses` (`use_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plant_uses`
--

LOCK TABLES `plant_uses` WRITE;
/*!40000 ALTER TABLE `plant_uses` DISABLE KEYS */;
INSERT INTO `plant_uses` VALUES (1,7,1,'Traditional',NULL),(2,7,2,'Traditional',NULL),(3,11,3,'Traditional',NULL),(4,11,4,'Traditional',NULL);
/*!40000 ALTER TABLE `plant_uses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plants`
--

DROP TABLE IF EXISTS `plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plants` (
  `plant_id` int NOT NULL AUTO_INCREMENT,
  `common_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scientific_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `family` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genus` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `species` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `habitat` text COLLATE utf8mb4_unicode_ci,
  `origin` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `distribution` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `traditional_uses` longtext COLLATE utf8mb4_unicode_ci,
  `conservation_status` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `toxicity` text COLLATE utf8mb4_unicode_ci,
  `edible` tinyint(1) DEFAULT '0',
  `medicinal` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`plant_id`),
  KEY `idx_common_name` (`common_name`),
  KEY `idx_scientific_name` (`scientific_name`),
  KEY `idx_family` (`family`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plants`
--

LOCK TABLES `plants` WRITE;
/*!40000 ALTER TABLE `plants` DISABLE KEYS */;
INSERT INTO `plants` VALUES (7,'Crofton weed','Ageratina adenophora','Asteraceae','','','','Thrives primarily in montane, subtropical, and warm temperate zones, typically at elevations between 1,000 m and 2,600 m above sea level.','Asia: India (notably the Himalayan regions like Himachal Pradesh and parts of the Northeast), China (Yunnan, Guizhou, Guangxi), Nepal, Bhutan, Myanmar, Thailand, Vietnam, Taiwan, and the Philippines.','','','','','images/plants/Ageratina_adenophora_Flower_2.jpg','',0,1,'2026-10-16 20:55:08'),(11,'Black-jack','Bidens pilosa','Asteraceae','Bidens','Bidens pilosa L.','Medicinal Plant','highly adaptable, sun-loving pioneer herb that dominates disturbed areas like roadsides, agricultural fields, and waste grounds globally from sea level up to 2,500 metres.','It has naturalised and spread aggressively throughout Africa, Asia, Australia, Europe, and the Pacific Islands.','In the Eastern Himalayan zone of Darjeeling (West Bengal)','','','','images/plants/Bidens_pilosa-Silent_Valley-2016-08-13-001.jpg','',0,1,'2026-10-16 21:48:46');
/*!40000 ALTER TABLE `plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `research_papers`
--

DROP TABLE IF EXISTS `research_papers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `research_papers` (
  `paper_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `authors` text COLLATE utf8mb4_unicode_ci,
  `journal` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `publication_year` year DEFAULT NULL,
  `doi` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paper_url` text COLLATE utf8mb4_unicode_ci,
  `abstract` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `research_papers`
--

LOCK TABLES `research_papers` WRITE;
/*!40000 ALTER TABLE `research_papers` DISABLE KEYS */;
/*!40000 ALTER TABLE `research_papers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institution` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` enum('Student','Researcher','Faculty','Admin') COLLATE utf8mb4_unicode_ci DEFAULT 'Student',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `otp_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'Ayush D','kazamaaaa','ayushsenpai6969@gmail.com','$2b$12$n9mywPNG3SB2ObEWmtWX0ecxEPd0Acx4avGI2.ZWvLMEaO0vrQgpy','Salesian College Autonomous','India','Admin','2026-07-07 10:08:32','$2b$12$dllOC7Zws4tQP4jlwD3jM.ddaQex3EuVJEs3wlwGBKDd6uzhSJKRC','2026-07-09 21:33:45'),(4,'Administrator','admin1','ayush.ad2736@gmail.com','$2b$12$BY/Q1TfLRsm.LJ7aZcijwu6X1zfHHbBK7P6W8YgZg//cld/SNMYvu','PhytoVault','India','Faculty','2026-07-08 10:12:41',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-17 21:58:24
