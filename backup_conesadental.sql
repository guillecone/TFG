-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: ConesaDental
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `citas`
--

DROP TABLE IF EXISTS `citas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `citas` (
  `id_cita` int NOT NULL AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `id_doctor` int NOT NULL,
  `fecha_cita` datetime NOT NULL,
  `estado` enum('Pendiente','Completada','Cancelada') DEFAULT 'Pendiente',
  PRIMARY KEY (`id_cita`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_doctor` (`id_doctor`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE,
  CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `doctores` (`id_doctor`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas`
--

LOCK TABLES `citas` WRITE;
/*!40000 ALTER TABLE `citas` DISABLE KEYS */;
INSERT INTO `citas` VALUES (1,1,1,'2024-03-01 10:00:00','Completada'),(2,2,2,'2024-03-02 14:30:00','Completada'),(3,3,1,'2024-03-03 09:00:00','Pendiente'),(4,4,3,'2024-03-04 11:15:00','Completada'),(5,5,1,'2024-03-01 09:00:00','Completada'),(6,6,2,'2024-03-02 11:30:00','Completada'),(7,7,1,'2024-03-03 15:00:00','Completada'),(8,8,3,'2024-03-04 10:45:00','Completada'),(9,5,1,'2024-03-01 09:00:00','Completada'),(10,6,2,'2024-03-02 11:30:00','Cancelada'),(11,7,1,'2024-03-03 15:00:00','Completada'),(12,8,3,'2024-03-04 10:45:00','Completada'),(13,5,1,'2024-03-01 09:00:00','Completada'),(14,6,2,'2024-03-02 11:30:00','Cancelada'),(15,7,1,'2024-03-03 15:00:00','Completada'),(16,8,3,'2024-03-04 10:45:00','Completada');
/*!40000 ALTER TABLE `citas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `costos_operativos`
--

DROP TABLE IF EXISTS `costos_operativos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `costos_operativos` (
  `id_costo` int NOT NULL AUTO_INCREMENT,
  `tipo_costo` enum('Insumos','Salarios','Alquiler','Otros') NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id_costo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `costos_operativos`
--

LOCK TABLES `costos_operativos` WRITE;
/*!40000 ALTER TABLE `costos_operativos` DISABLE KEYS */;
INSERT INTO `costos_operativos` VALUES (1,'Insumos',500.00,'2024-03-01'),(2,'Salarios',3000.00,'2024-03-01'),(3,'Alquiler',1200.00,'2024-03-01'),(4,'Otros',200.00,'2024-03-01');
/*!40000 ALTER TABLE `costos_operativos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctores`
--

DROP TABLE IF EXISTS `doctores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctores` (
  `id_doctor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_doctor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctores`
--

LOCK TABLES `doctores` WRITE;
/*!40000 ALTER TABLE `doctores` DISABLE KEYS */;
INSERT INTO `doctores` VALUES (1,'Dr. Luis','Ramírez','Ortodoncia'),(2,'Dra. Sofía','Martínez','Implantología'),(3,'Dr. Andrés','Hernández','Endodoncia');
/*!40000 ALTER TABLE `doctores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materiales`
--

DROP TABLE IF EXISTS `materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiales` (
  `id_material` int NOT NULL AUTO_INCREMENT,
  `nombre_material` varchar(100) NOT NULL,
  `stock_actual` int NOT NULL,
  `stock_minimo` int NOT NULL,
  `fecha_actualizacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `id_proveedor` int DEFAULT NULL,
  PRIMARY KEY (`id_material`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `materiales_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiales`
--

LOCK TABLES `materiales` WRITE;
/*!40000 ALTER TABLE `materiales` DISABLE KEYS */;
INSERT INTO `materiales` VALUES (1,'Anestesia',20,5,'2025-03-10 09:03:11',NULL),(2,'Material de Empaste',15,3,'2025-03-10 09:03:11',NULL),(3,'Hilo de sutura',10,2,'2025-03-10 09:03:11',NULL),(4,'Guantes',50,10,'2025-03-10 09:03:11',NULL),(5,'Anestesia',20,5,'2025-03-10 11:17:52',1),(6,'Material de Empaste',15,3,'2025-03-10 11:17:52',2),(7,'Hilo de sutura',10,2,'2025-03-10 11:17:52',3),(8,'Guantes',50,10,'2025-03-10 11:17:52',1),(9,'Anestesia',20,5,'2025-03-10 11:18:22',1),(10,'Material de Empaste',15,3,'2025-03-10 11:18:22',2),(11,'Hilo de sutura',10,2,'2025-03-10 11:18:22',3),(12,'Guantes',50,10,'2025-03-10 11:18:22',1);
/*!40000 ALTER TABLE `materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes` (
  `id_paciente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_paciente`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
INSERT INTO `pacientes` VALUES (1,'Juan','Pérez','1990-05-10','2025-03-10 09:03:11','123456789','juan.perez@email.com'),(2,'María','Gómez','1985-09-22','2025-03-10 09:03:11','987654321','maria.gomez@email.com'),(3,'Carlos','Fernández','1995-12-15','2025-03-10 09:03:11','654321987','carlos.fernandez@email.com'),(4,'Ana','López','1988-07-08','2025-03-10 09:03:11','321654987','ana.lopez@email.com'),(5,'Juan','Pérez','1990-05-10','2024-03-01 10:15:00','123456789','juan.perez@email.com'),(6,'María','Gómez','1985-09-22','2024-03-02 14:30:00','987654321','maria.gomez@email.com'),(7,'Carlos','Fernández','1995-12-15','2024-03-05 09:00:00','654321987','carlos.fernandez@email.com'),(8,'Ana','López','1988-07-08','2024-03-08 11:45:00','321654987','ana.lopez@email.com');
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre_proveedor` varchar(255) NOT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Proveedor Dental S.A.'),(2,'Dentales Express'),(3,'Distribuidora Médica'),(4,'Proveedor Dental S.A.'),(5,'Dentales Express'),(6,'Distribuidora Medica');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tratamientos`
--

DROP TABLE IF EXISTS `tratamientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tratamientos` (
  `id_tratamiento` int NOT NULL AUTO_INCREMENT,
  `nombre_tratamiento` varchar(100) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_tratamiento`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tratamientos`
--

LOCK TABLES `tratamientos` WRITE;
/*!40000 ALTER TABLE `tratamientos` DISABLE KEYS */;
INSERT INTO `tratamientos` VALUES (1,'Limpieza Dental',50.00),(2,'Empaste',80.00),(3,'Ortodoncia',500.00),(4,'Implante Dental',1000.00),(5,'Limpieza Dental',50.00),(6,'Empaste',80.00),(7,'Ortodoncia',500.00),(8,'Implante Dental',1000.00),(9,'Limpieza Dental',50.00),(10,'Empaste',80.00),(11,'Ortodoncia',500.00),(12,'Implante Dental',1000.00);
/*!40000 ALTER TABLE `tratamientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tratamientos_realizados`
--

DROP TABLE IF EXISTS `tratamientos_realizados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tratamientos_realizados` (
  `id_tratamiento_realizado` int NOT NULL AUTO_INCREMENT,
  `id_paciente` int NOT NULL,
  `id_tratamiento` int NOT NULL,
  `id_doctor` int NOT NULL,
  `fecha_tratamiento` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_tratamiento_realizado`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_tratamiento` (`id_tratamiento`),
  KEY `id_doctor` (`id_doctor`),
  CONSTRAINT `tratamientos_realizados_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON DELETE CASCADE,
  CONSTRAINT `tratamientos_realizados_ibfk_2` FOREIGN KEY (`id_tratamiento`) REFERENCES `tratamientos` (`id_tratamiento`) ON DELETE CASCADE,
  CONSTRAINT `tratamientos_realizados_ibfk_3` FOREIGN KEY (`id_doctor`) REFERENCES `doctores` (`id_doctor`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tratamientos_realizados`
--

LOCK TABLES `tratamientos_realizados` WRITE;
/*!40000 ALTER TABLE `tratamientos_realizados` DISABLE KEYS */;
INSERT INTO `tratamientos_realizados` VALUES (1,1,1,1,'2024-03-01 10:30:00'),(2,2,3,2,'2024-03-02 15:00:00'),(3,3,2,1,'2024-03-05 09:30:00'),(4,4,4,3,'2024-03-04 12:00:00'),(5,5,1,1,'2024-03-01 10:30:00'),(6,6,2,2,'2024-03-02 11:00:00'),(7,7,3,1,'2024-03-03 15:00:00'),(8,8,4,3,'2024-03-04 12:30:00'),(9,5,1,1,'2024-03-01 10:30:00'),(10,6,2,2,'2024-03-02 11:00:00'),(11,7,3,1,'2024-03-03 15:00:00'),(12,8,4,3,'2024-03-04 12:30:00');
/*!40000 ALTER TABLE `tratamientos_realizados` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-10 12:18:50
