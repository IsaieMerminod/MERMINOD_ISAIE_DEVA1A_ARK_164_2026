-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 28 avr. 2026 à 14:17
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS merminod_isaie_deva1a_ark_164_2026;
CREATE DATABASE IF NOT EXISTS merminod_isaie_deva1a_ark_164_2026;
USE merminod_isaie_deva1a_ark_164_2026;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `merminod_isaie_deva1a_ark_164_2026`
--

-- --------------------------------------------------------

--
-- Structure de la table `aliments`
--

CREATE TABLE `aliments` (
  `ID_Aliment` int(11) NOT NULL,
  `Nom` varchar(100) NOT NULL,
  `Efficacite_tame` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `aliments`
--

INSERT INTO `aliments` (`ID_Aliment`, `Nom`, `Efficacite_tame`) VALUES
(1, 'Kibble Exceptionnelle', 100.00),
(2, 'Kibble Supérieure', 95.00),
(3, 'Viande de mouton', 85.00),
(4, 'Viande supérieure crue', 70.00),
(5, 'Viande crue', 50.00),
(6, 'Mejoberry', 30.00),
(7, 'Légumes', 45.00);

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `ID_Cat` int(11) NOT NULL,
  `Nom_categorie` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`ID_Cat`, `Nom_categorie`) VALUES
(1, 'Terrestre'),
(2, 'Volant'),
(3, 'Aquatique');

-- --------------------------------------------------------

--
-- Structure de la table `creatures`
--

CREATE TABLE `creatures` (
  `ID_Creature` int(11) NOT NULL,
  `Nom` varchar(100) NOT NULL,
  `Torpeur_base` int(11) DEFAULT NULL,
  `Regime_alimentaire` varchar(50) DEFAULT NULL,
  `ID_Cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `creatures`
--

INSERT INTO `creatures` (`ID_Creature`, `Nom`, `Torpeur_base`, `Regime_alimentaire`, `ID_Cat`) VALUES
(1, 'Rex', 1550, 'Carnivore', 1),
(2, 'Raptor', 180, 'Carnivore', 1),
(3, 'Argentavis', 600, 'Carnivore', 2),
(4, 'Spinosaur', 850, 'Carnivore', 1),
(5, 'Giganotosaurus', 80000, 'Carnivore', 1),
(6, 'Dodo', 30, 'Herbivore', 1),
(7, 'Therizinosaur', 900, 'Herbivore', 1),
(8, 'Mosasaur', 3000, 'Carnivore', 3);

-- --------------------------------------------------------

--
-- Structure de la table `creature_aliment`
--

CREATE TABLE `creature_aliment` (
  `ID_Creature` int(11) NOT NULL,
  `ID_Aliment` int(11) NOT NULL,
  `Quantite_requise` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `creature_aliment`
--

INSERT INTO `creature_aliment` (`ID_Creature`, `ID_Aliment`, `Quantite_requise`) VALUES
(1, 1, 17),
(1, 4, 45),
(3, 3, 12),
(5, 1, 30),
(6, 6, 20),
(7, 7, 150),
(8, 4, 100);

-- --------------------------------------------------------

--
-- Structure de la table `creature_localisation`
--

CREATE TABLE `creature_localisation` (
  `ID_Creature` int(11) NOT NULL,
  `ID_Loc` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `favoris`
--

CREATE TABLE `favoris` (
  `ID_Fav` int(11) NOT NULL,
  `Date_ajout` datetime DEFAULT current_timestamp(),
  `ID_User` int(11) DEFAULT NULL,
  `ID_Creature` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `localisations`
--

CREATE TABLE `localisations` (
  `ID_Loc` int(11) NOT NULL,
  `Latitude` decimal(10,8) DEFAULT NULL,
  `Longitude` decimal(11,8) DEFAULT NULL,
  `ID_Map` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `maps`
--

CREATE TABLE `maps` (
  `ID_Map` int(11) NOT NULL,
  `Nom_map` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `maps`
--

INSERT INTO `maps` (`ID_Map`, `Nom_map`) VALUES
(1, 'The Island'),
(2, 'Scorched Earth'),
(3, 'Aberration'),
(4, 'Extinction');

-- --------------------------------------------------------

--
-- Structure de la table `photos`
--

CREATE TABLE `photos` (
  `ID_Photo` int(11) NOT NULL,
  `URL_image` varchar(255) NOT NULL,
  `ID_Creature` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `signalements`
--

CREATE TABLE `signalements` (
  `ID_Sign` int(11) NOT NULL,
  `Type_erreur` varchar(50) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Statut` varchar(20) DEFAULT 'En attente',
  `ID_User` int(11) DEFAULT NULL,
  `ID_Creature` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `ID_User` int(11) NOT NULL,
  `Pseudo` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Mot_de_passe` varchar(255) NOT NULL,
  `Date_inscription` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `aliments`
--
ALTER TABLE `aliments`
  ADD PRIMARY KEY (`ID_Aliment`);

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`ID_Cat`);

--
-- Index pour la table `creatures`
--
ALTER TABLE `creatures`
  ADD PRIMARY KEY (`ID_Creature`),
  ADD KEY `ID_Cat` (`ID_Cat`);

--
-- Index pour la table `creature_aliment`
--
ALTER TABLE `creature_aliment`
  ADD PRIMARY KEY (`ID_Creature`,`ID_Aliment`),
  ADD KEY `ID_Aliment` (`ID_Aliment`);

--
-- Index pour la table `creature_localisation`
--
ALTER TABLE `creature_localisation`
  ADD PRIMARY KEY (`ID_Creature`,`ID_Loc`),
  ADD KEY `ID_Loc` (`ID_Loc`);

--
-- Index pour la table `favoris`
--
ALTER TABLE `favoris`
  ADD PRIMARY KEY (`ID_Fav`),
  ADD KEY `ID_User` (`ID_User`),
  ADD KEY `ID_Creature` (`ID_Creature`);

--
-- Index pour la table `localisations`
--
ALTER TABLE `localisations`
  ADD PRIMARY KEY (`ID_Loc`),
  ADD KEY `ID_Map` (`ID_Map`);

--
-- Index pour la table `maps`
--
ALTER TABLE `maps`
  ADD PRIMARY KEY (`ID_Map`);

--
-- Index pour la table `photos`
--
ALTER TABLE `photos`
  ADD PRIMARY KEY (`ID_Photo`),
  ADD KEY `ID_Creature` (`ID_Creature`);

--
-- Index pour la table `signalements`
--
ALTER TABLE `signalements`
  ADD PRIMARY KEY (`ID_Sign`),
  ADD KEY `ID_User` (`ID_User`),
  ADD KEY `ID_Creature` (`ID_Creature`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`ID_User`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `aliments`
--
ALTER TABLE `aliments`
  MODIFY `ID_Aliment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `ID_Cat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `creatures`
--
ALTER TABLE `creatures`
  MODIFY `ID_Creature` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `favoris`
--
ALTER TABLE `favoris`
  MODIFY `ID_Fav` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `localisations`
--
ALTER TABLE `localisations`
  MODIFY `ID_Loc` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `maps`
--
ALTER TABLE `maps`
  MODIFY `ID_Map` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `photos`
--
ALTER TABLE `photos`
  MODIFY `ID_Photo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `signalements`
--
ALTER TABLE `signalements`
  MODIFY `ID_Sign` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `ID_User` int(11) NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `creatures`
--
ALTER TABLE `creatures`
  ADD CONSTRAINT `creatures_ibfk_1` FOREIGN KEY (`ID_Cat`) REFERENCES `categories` (`ID_Cat`) ON DELETE SET NULL;

--
-- Contraintes pour la table `creature_aliment`
--
ALTER TABLE `creature_aliment`
  ADD CONSTRAINT `creature_aliment_ibfk_1` FOREIGN KEY (`ID_Creature`) REFERENCES `creatures` (`ID_Creature`) ON DELETE CASCADE,
  ADD CONSTRAINT `creature_aliment_ibfk_2` FOREIGN KEY (`ID_Aliment`) REFERENCES `aliments` (`ID_Aliment`) ON DELETE CASCADE;

--
-- Contraintes pour la table `creature_localisation`
--
ALTER TABLE `creature_localisation`
  ADD CONSTRAINT `creature_localisation_ibfk_1` FOREIGN KEY (`ID_Creature`) REFERENCES `creatures` (`ID_Creature`) ON DELETE CASCADE,
  ADD CONSTRAINT `creature_localisation_ibfk_2` FOREIGN KEY (`ID_Loc`) REFERENCES `localisations` (`ID_Loc`) ON DELETE CASCADE;

--
-- Contraintes pour la table `favoris`
--
ALTER TABLE `favoris`
  ADD CONSTRAINT `favoris_ibfk_1` FOREIGN KEY (`ID_User`) REFERENCES `utilisateurs` (`ID_User`) ON DELETE CASCADE,
  ADD CONSTRAINT `favoris_ibfk_2` FOREIGN KEY (`ID_Creature`) REFERENCES `creatures` (`ID_Creature`) ON DELETE CASCADE;

--
-- Contraintes pour la table `localisations`
--
ALTER TABLE `localisations`
  ADD CONSTRAINT `localisations_ibfk_1` FOREIGN KEY (`ID_Map`) REFERENCES `maps` (`ID_Map`) ON DELETE CASCADE;

--
-- Contraintes pour la table `photos`
--
ALTER TABLE `photos`
  ADD CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`ID_Creature`) REFERENCES `creatures` (`ID_Creature`) ON DELETE CASCADE;

--
-- Contraintes pour la table `signalements`
--
ALTER TABLE `signalements`
  ADD CONSTRAINT `signalements_ibfk_1` FOREIGN KEY (`ID_User`) REFERENCES `utilisateurs` (`ID_User`) ON DELETE CASCADE,
  ADD CONSTRAINT `signalements_ibfk_2` FOREIGN KEY (`ID_Creature`) REFERENCES `creatures` (`ID_Creature`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
