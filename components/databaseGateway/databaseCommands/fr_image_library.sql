-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2024 at 03:08 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fr_image_library`
--
CREATE DATABASE IF NOT EXISTS `fr_image_library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fr_image_library`;

-- --------------------------------------------------------

--
-- Table structure for table `image_library_index`
--

DROP TABLE IF EXISTS `image_library_index`;
CREATE TABLE `image_library_index` (
  `id` int(11) NOT NULL,
  `img_name` varchar(15) NOT NULL,
  `tagged` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `image_library_tagged_faces`
--

DROP TABLE IF EXISTS `image_library_tagged_faces`;
CREATE TABLE `image_library_tagged_faces` (
  `tagged_face_id` int(11) NOT NULL,
  `img_name` varchar(15) NOT NULL,
  `profile_uid` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `profile_index`
--

DROP TABLE IF EXISTS `profile_index`;
CREATE TABLE `profile_index` (
  `profile_id` int(11) NOT NULL,
  `profile_uid` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `profile_mapper`
--

DROP TABLE IF EXISTS `profile_mapper`;
CREATE TABLE `profile_mapper` (
  `mapper_id` int(11) NOT NULL,
  `profile_uid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `profile_tmp_index_frdb`
--

DROP TABLE IF EXISTS `profile_tmp_index_frdb`;
CREATE TABLE `profile_tmp_index_frdb` (
  `profile_tmp_id` int(11) NOT NULL,
  `profile_tmp_uid` varchar(255) NOT NULL,
  `profile_tmp_src` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `image_library_index`
--
ALTER TABLE `image_library_index`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `img_name` (`img_name`);

--
-- Indexes for table `image_library_tagged_faces`
--
ALTER TABLE `image_library_tagged_faces`
  ADD PRIMARY KEY (`tagged_face_id`);

--
-- Indexes for table `profile_index`
--
ALTER TABLE `profile_index`
  ADD PRIMARY KEY (`profile_id`),
  ADD UNIQUE KEY `profile_uid` (`profile_uid`);

--
-- Indexes for table `profile_mapper`
--
ALTER TABLE `profile_mapper`
  ADD PRIMARY KEY (`mapper_id`),
  ADD UNIQUE KEY `profile_uid` (`profile_uid`);

--
-- Indexes for table `profile_tmp_index_frdb`
--
ALTER TABLE `profile_tmp_index_frdb`
  ADD PRIMARY KEY (`profile_tmp_id`),
  ADD UNIQUE KEY `profile_tmp_uid` (`profile_tmp_uid`),
  ADD UNIQUE KEY `profile_tmp_src` (`profile_tmp_src`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `image_library_index`
--
ALTER TABLE `image_library_index`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `image_library_tagged_faces`
--
ALTER TABLE `image_library_tagged_faces`
  MODIFY `tagged_face_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `profile_index`
--
ALTER TABLE `profile_index`
  MODIFY `profile_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `profile_mapper`
--
ALTER TABLE `profile_mapper`
  MODIFY `mapper_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

--
-- AUTO_INCREMENT for table `profile_tmp_index_frdb`
--
ALTER TABLE `profile_tmp_index_frdb`
  MODIFY `profile_tmp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
