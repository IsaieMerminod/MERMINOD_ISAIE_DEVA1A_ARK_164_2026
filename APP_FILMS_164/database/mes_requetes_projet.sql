-- Requête pour afficher toutes les Maps
SELECT ID_Map, Nom_map FROM Maps ORDER BY ID_Map ASC;

-- Requête pour ajouter une nouvelle Map
INSERT INTO Maps (ID_Map, Nom_map) VALUES (NULL, 'Scorched Earth');

-- Requête complexe avec jointure pour afficher les dinos et leurs aliments
SELECT Creatures.ID_Creature, Creatures.Nom, Creatures.Torpeur_base, Creatures.Regime_alimentaire,
GROUP_CONCAT(Aliments.Nom) as AlimentsCreature FROM creature_aliment
RIGHT JOIN Creatures ON Creatures.ID_Creature = creature_aliment.ID_Creature
LEFT JOIN Aliments ON Aliments.ID_Aliment = creature_aliment.ID_Aliment
GROUP BY Creatures.ID_Creature;