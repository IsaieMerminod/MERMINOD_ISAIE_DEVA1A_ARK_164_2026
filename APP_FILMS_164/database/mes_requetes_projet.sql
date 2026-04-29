-- ==========================================================
-- REQUÊTES SQL DU PROJET ARK_ASCENDED_HUB
-- Auteur : Isaïe Merminod
-- ==========================================================

-- 1. Liste simple : Afficher toutes les cartes disponibles
SELECT Nom_map FROM maps ORDER BY ID_Map ASC;

-- 2. Jointure 1:N : Afficher les créatures avec le nom de leur catégorie (Terrestre, etc.)
SELECT creatures.Nom, categories.Nom_categorie
FROM creatures
JOIN categories ON creatures.ID_Cat = categories.ID_Cat;

-- 3. Requête complexe N:M : Dinosaures et leurs aliments préférés avec quantités
-- C'est la requête qui alimente la page "Dinos & Aliments"
SELECT creatures.Nom AS Dinosaure, aliments.Nom AS Nourriture, creature_aliment.Quantite_requise
FROM creature_aliment
JOIN creatures ON creature_aliment.ID_Creature = creatures.ID_Creature
JOIN aliments ON creature_aliment.ID_Aliment = aliments.ID_Aliment
ORDER BY creatures.Nom ASC;

-- 4. Agrégation : Trouver la créature qui a la plus grosse torpeur de base (Le Giganotosaurus)
SELECT Nom, Torpeur_base
FROM creatures
WHERE Torpeur_base = (SELECT MAX(Torpeur_base) FROM creatures);

-- 5. Filtre : Afficher uniquement les carnivores qui vivent dans l'eau (Aquatique)
SELECT Nom FROM creatures
WHERE Regime_alimentaire = 'Carnivore' AND ID_Cat = 3;