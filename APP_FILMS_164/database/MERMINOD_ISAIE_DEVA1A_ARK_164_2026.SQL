-- OM 2021.02.17
-- FICHIER MYSQL POUR LE PROJET ARK - ISAIE MERMINOD
-- Destruction de la BD si elle existe pour repartir à zéro
DROP DATABASE IF EXISTS MERMINOD_ISAIE_DEVA1A_ARK_164_2026;

-- Création de la base de données propre au projet
CREATE DATABASE IF NOT EXISTS MERMINOD_ISAIE_DEVA1A_ARK_164_2026;

-- Utilisation de cette base de données
USE MERMINOD_ISAIE_DEVA1A_ARK_164_2026;

-- 1. Tables indépendantes (sans clés étrangères)
CREATE TABLE Utilisateurs (
    ID_User INT AUTO_INCREMENT PRIMARY KEY,
    Pseudo VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Mot_de_passe VARCHAR(255) NOT NULL,
    Date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
    ID_Cat INT AUTO_INCREMENT PRIMARY KEY,
    Nom_categorie VARCHAR(50) NOT NULL
);

CREATE TABLE Aliments (
    ID_Aliment INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Efficacite_tame DECIMAL(5, 2)
);

CREATE TABLE Maps (
    ID_Map INT AUTO_INCREMENT PRIMARY KEY,
    Nom_map VARCHAR(100) NOT NULL
);

-- 2. Tables avec clés étrangères simples
CREATE TABLE Creatures (
    ID_Creature INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Torpeur_base INT,
    Regime_alimentaire VARCHAR(50),
    ID_Cat INT,
    FOREIGN KEY (ID_Cat) REFERENCES Categories(ID_Cat) ON DELETE SET NULL
);

CREATE TABLE Localisations (
    ID_Loc INT AUTO_INCREMENT PRIMARY KEY,
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(11, 8),
    ID_Map INT,
    FOREIGN KEY (ID_Map) REFERENCES Maps(ID_Map) ON DELETE CASCADE
);

CREATE TABLE Photos (
    ID_Photo INT AUTO_INCREMENT PRIMARY KEY,
    URL_image VARCHAR(255) NOT NULL,
    ID_Creature INT,
    FOREIGN KEY (ID_Creature) REFERENCES Creatures(ID_Creature) ON DELETE CASCADE
);

-- 3. Tables de fonctionnalités (Favoris / Signalements)
CREATE TABLE Favoris (
    ID_Fav INT AUTO_INCREMENT PRIMARY KEY,
    Date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
    ID_User INT,
    ID_Creature INT,
    FOREIGN KEY (ID_User) REFERENCES Utilisateurs(ID_User) ON DELETE CASCADE,
    FOREIGN KEY (ID_Creature) REFERENCES Creatures(ID_Creature) ON DELETE CASCADE
);

CREATE TABLE Signalements (
    ID_Sign INT AUTO_INCREMENT PRIMARY KEY,
    Type_erreur VARCHAR(50),
    Description TEXT,
    Statut VARCHAR(20) DEFAULT 'En attente',
    ID_User INT,
    ID_Creature INT,
    FOREIGN KEY (ID_User) REFERENCES Utilisateurs(ID_User) ON DELETE CASCADE,
    FOREIGN KEY (ID_Creature) REFERENCES Creatures(ID_Creature) ON DELETE CASCADE
);

-- 4. Tables intermédiaires (N,N) avec clés composites
CREATE TABLE creature_aliment (
    ID_Creature INT,
    ID_Aliment INT,
    Quantite_requise INT DEFAULT 1,
    PRIMARY KEY (ID_Creature, ID_Aliment),
    FOREIGN KEY (ID_Creature) REFERENCES Creatures(ID_Creature) ON DELETE CASCADE,
    FOREIGN KEY (ID_Aliment) REFERENCES Aliments(ID_Aliment) ON DELETE CASCADE
);

CREATE TABLE creature_localisation (
    ID_Creature INT,
    ID_Loc INT,
    PRIMARY KEY (ID_Creature, ID_Loc),
    FOREIGN KEY (ID_Creature) REFERENCES Creatures(ID_Creature) ON DELETE CASCADE,
    FOREIGN KEY (ID_Loc) REFERENCES Localisations(ID_Loc) ON DELETE CASCADE
);