-----------  Index ------------------
-- Cle etrangere 
CREATE INDEX idx_instance_idclientfinal ON Instance(Id_ClientFinal);
CREATE INDEX idx_incident_numserie_nom ON Incident(Num_Serie, Nom);
CREATE INDEX idx_redemarrage_numserie_nom ON Redemarrage(Num_Serie, Nom);
CREATE INDEX idx_disques_numserie_nom ON Disques(Num_Serie, Nom);
CREATE INDEX idx_installation_numserie_nom ON Installation(Num_Serie, Nom);
CREATE INDEX idx_installation_idscript ON Installation(Id_Script);

-- Index sur les colonnes souvent filtrées
CREATE INDEX idx_instance_etat ON Instance(Etat);
CREATE INDEX idx_instance_nom ON Instance(Nom);
CREATE INDEX idx_instance_numserie ON Instance(Num_Serie);


-------------- Vue ----------------------
-- Vue pour le prestataire 100002
CREATE VIEW v_instances_prestataire_100002 AS
SELECT i.*
FROM Instance i
JOIN Client_Final c ON i.Id_ClientFinal = c.Id_ClientFinal
WHERE c.SIRET = 100002;

-- Client pour la vue, acces a sa vue uniquement
CREATE USER client_alpha WITH PASSWORD 'password_alpha';
GRANT SELECT ON v_instances_prestataire_100002 TO client_alpha;
REVOKE ALL ON Instance FROM client_alpha;
REVOKE ALL ON Client_Final FROM client_alpha;




------------------- Requêtes et Triggers (a adapter) --------------
-- 1. Liste des instances d’un client prestataire donné
SELECT i.*
FROM Instance i
JOIN Client_Final c ON i.Id_ClientFinal = c.Id_ClientFinal
WHERE c.SIRET = 100002;

-- 2. Liste des incidents pour une instance donnée
SELECT *
FROM Incident
WHERE Num_Serie = 10010 AND Nom = 'AlphaA-01';

-- 3. Liste des instances qui n’ont jamais été redémarrées manuellement
SELECT i.*
FROM Instance i
WHERE NOT EXISTS (
  SELECT 1 FROM Redemarrage r
  WHERE r.Num_Serie = i.Num_Serie AND r.Nom = i.Nom AND r.Motif ILIKE '%manuel%'
);


-- 4. Liste des instances d’un client prestataire donné à récupérer
--  date d’installation + durée (en jours ou mois) < NOW
SELECT i.*
FROM Instance i
JOIN Client_Final c ON i.Id_ClientFinal = c.Id_ClientFinal
WHERE c.SIRET = 100002
  AND (i.MaterielRecupere = TRUE OR i.DateInstallation + INTERVAL '730 days' < NOW());

-- 5. Historique des installations pour une instance donnée
SELECT ins.Num_Serie, ins.Nom, s.NomScript, ins.DateInstal,
       t.Nom AS Technicien, c.Nom AS ClientFinal
FROM Installation ins
JOIN ScriptInstalle s ON ins.Id_Script = s.Id_Script
JOIN Instance i ON ins.Num_Serie = i.Num_Serie AND ins.Nom = i.Nom
JOIN Client_Final c ON i.Id_ClientFinal = c.Id_ClientFinal
LEFT JOIN Incident inc ON inc.Num_Serie = i.Num_Serie AND inc.Nom = i.Nom
LEFT JOIN Technicien t ON inc.Id_Tech = t.Id_Tech
WHERE ins.Num_Serie = 10010 AND ins.Nom = 'AlphaA-01'
ORDER BY ins.DateInstal;


-- 6. Trigger ou procédure stockée : instances redémarrées manuellement plus de 5 fois
-- Vue pour compter les redémarrages manuels
CREATE OR REPLACE VIEW v_instances_redemarrage_5plus AS
SELECT Num_Serie, Nom, COUNT(*) as nb_redemarrages
FROM Redemarrage
WHERE Motif ILIKE '%manuel%'
GROUP BY Num_Serie, Nom
HAVING COUNT(*) > 5;

-- Procedure stocke
CREATE OR REPLACE FUNCTION liste_instances_redemarrage_5plus()
RETURNS TABLE(Num_Serie INT, Nom VARCHAR, nb_redemarrages INT)
AS $$
BEGIN
  RETURN QUERY
    SELECT r.Num_Serie, r.Nom, COUNT(*)::INT as nb_redemarrages
    FROM Redemarrage r
    WHERE r.Motif ILIKE '%manuel%'
    GROUP BY r.Num_Serie, r.Nom
    HAVING COUNT(*) > 5;
END;
$$ LANGUAGE plpgsql;

-- Executer
SELECT * FROM liste_instances_redemarrage_5plus();



