-- phpMyAdmin SQL Dump
-- version 4.3.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Erstellungszeit: 16. Jan 2017 um 16:10
-- Server-Version: 5.6.24
-- PHP-Version: 5.6.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `scibib`
--
CREATE DATABASE IF NOT EXISTS `scibib` DEFAULT CHARACTER SET utf8 COLLATE utf8_german2_ci;
USE `scibib`;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `authors`
--

CREATE TABLE IF NOT EXISTS `authors` (
  `id` int(11) NOT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `forename` varchar(255) DEFAULT NULL,
  `cleanname` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=762 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `authors_publications`
--

CREATE TABLE IF NOT EXISTS `authors_publications` (
  `id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `publication_id` int(11) NOT NULL,
  `position` int(11) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=9907 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cake_d_c_users_phinxlog`
--

CREATE TABLE IF NOT EXISTS `cake_d_c_users_phinxlog` (
  `version` bigint(20) NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `lft` int(11) DEFAULT NULL,
  `rght` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `categories_publications`
--

CREATE TABLE IF NOT EXISTS `categories_publications` (
  `id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `publication_id` int(11) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=11736 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `chairs`
--

CREATE TABLE IF NOT EXISTS `chairs` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `chairs_publications`
--

CREATE TABLE IF NOT EXISTS `chairs_publications` (
  `id` int(11) NOT NULL,
  `chair_id` int(11) NOT NULL,
  `publication_id` int(11) NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=2350 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `copyrights`
--

CREATE TABLE IF NOT EXISTS `copyrights` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `disclaimer` mediumtext,
  `created` date DEFAULT NULL,
  `modified` date DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `documents`
--

CREATE TABLE IF NOT EXISTS `documents` (
  `id` int(11) NOT NULL,
  `publication_id` int(11) DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `remote` tinyint(1) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=667 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `keywords`
--

CREATE TABLE IF NOT EXISTS `keywords` (
  `id` int(11) NOT NULL,
  `publication_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=156 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posts`
--

CREATE TABLE IF NOT EXISTS `posts` (
  `id` int(10) unsigned NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `body` text,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `publications`
--

CREATE TABLE IF NOT EXISTS `publications` (
  `id` int(11) NOT NULL,
  `address` mediumtext,
  `booktitle` varchar(255) DEFAULT NULL,
  `chapter` int(11) DEFAULT NULL,
  `edition` varchar(255) DEFAULT NULL,
  `editor` varchar(255) DEFAULT NULL,
  `howpublished` mediumtext,
  `institution` varchar(255) DEFAULT NULL,
  `journal` varchar(255) DEFAULT NULL,
  `month` varchar(3) DEFAULT NULL,
  `note` mediumtext,
  `number` varchar(255) DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `pages` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `series` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `volume` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `doi` varchar(255) DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `citename` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `published` tinyint(1) DEFAULT NULL,
  `submitted` tinyint(1) DEFAULT NULL,
  `public` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `copyright_id` int(11) DEFAULT NULL,
  `type` enum('Inproceedings','Article','Techreport','Inbook','Book','Booklet','Conference','Incollection','Manual','Masterthesis','Misc','PhDThesis','Proceedings','Unpublished') DEFAULT NULL,
  `thumb` varchar(255) DEFAULT NULL,
  `mainfile` mediumtext,
  `publicationdate` date DEFAULT NULL,
  `kops` varchar(255) DEFAULT NULL,
  `abstract` text,
  `abstractphoto` varchar(255) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=788 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` char(36) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `token_expires` datetime DEFAULT NULL,
  `api_token` varchar(255) DEFAULT NULL,
  `activation_date` datetime DEFAULT NULL,
  `tos_date` datetime DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `role` varchar(255) DEFAULT 'user',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `authors_publications`
--
ALTER TABLE `authors_publications`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `cake_d_c_users_phinxlog`
--
ALTER TABLE `cake_d_c_users_phinxlog`
  ADD PRIMARY KEY (`version`);

--
-- Indizes für die Tabelle `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `categories_publications`
--
ALTER TABLE `categories_publications`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `chairs`
--
ALTER TABLE `chairs`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `chairs_publications`
--
ALTER TABLE `chairs_publications`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `copyrights`
--
ALTER TABLE `copyrights`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `keywords`
--
ALTER TABLE `keywords`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `publications`
--
ALTER TABLE `publications`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `citename` (`citename`), ADD KEY `copyright_id` (`copyright_id`), ADD KEY `publicationdate_idx` (`publicationdate`);

--
-- Indizes für die Tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `authors`
--
ALTER TABLE `authors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `authors_publications`
--
ALTER TABLE `authors_publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `categories_publications`
--
ALTER TABLE `categories_publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `chairs`
--
ALTER TABLE `chairs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `chairs_publications`
--
ALTER TABLE `chairs_publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `copyrights`
--
ALTER TABLE `copyrights`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `keywords`
--
ALTER TABLE `keywords`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
--
-- AUTO_INCREMENT für Tabelle `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(10) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT für Tabelle `publications`
--
ALTER TABLE `publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
