-- 1. Prestataires (5 + NFL IT) --
INSERT INTO Prestataire (SIRET, Nom, Adresse, Contact) VALUES
(100001, 'NFL IT', '1 Avenue NFL, Kansas City', 'Roger Goodell'),
(100002, 'Alpha Services', '10 Rue Alpha, Paris', 'Alice Martin'),
(100003, 'Beta Solutions', '20 Rue Beta, Lyon', 'Bob Dubois'),
(100004, 'Gamma Tech', '30 Rue Gamma, Marseille', 'Carole Petit'),
(100005, 'Delta IT', '40 Rue Delta, Lille', 'David Grand'),
(100006, 'Epsilon Group', '50 Rue Epsilon, Toulouse', 'Eva Bonnet');


-- 2. Clients finaux (2 par prestataire, sauf NFL IT) --
INSERT INTO Client_Final (Nom, Adresse, SIRET) VALUES
-- Alpha Services
('ClientAlphaA', '1 Place AlphaA, Paris', 100002),
('ClientAlphaB', '2 Place AlphaB, Paris', 100002),
-- Beta Solutions
('ClientBetaA', '1 Avenue BetaA, Lyon', 100003),
('ClientBetaB', '2 Avenue BetaB, Lyon', 100003),
-- Gamma Tech
('ClientGammaA', '1 Boulevard GammaA, Marseille', 100004),
('ClientGammaB', '2 Boulevard GammaB, Marseille', 100004),
-- Delta IT
('ClientDeltaA', '1 Impasse DeltaA, Lille', 100005),
('ClientDeltaB', '2 Impasse DeltaB, Lille', 100005),
-- Epsilon Group
('ClientEpsilonA', '1 Chemin EpsilonA, Toulouse', 100006),
('ClientEpsilonB', '2 Chemin EpsilonB, Toulouse', 100006);


-- 3. Techniciens --
INSERT INTO Technicien (Nom, Role) VALUES
('Maxime Leroy', 'Support'),
('Sarah Garnier', 'Intégrateur');


-- 4. Instances (2 franchises NFL + 10 clients finaux) --
-- franchises NFL (pas de client final)
INSERT INTO Instance (Num_Serie, Nom, RetourMateriel, AdresseIP, AdresseIP_VPN, Etat, DateInstallation, DatePeremption, NumeroLicence, MaterielRecupere, VersionApp, VersionOS, TypeMateriel, CPU, RAM, Id_ClientFinal)
VALUES
(20001, 'FranchiseA', NULL, '10.10.1.1', '192.168.10.1', 'connectee', NOW(), NULL, 1010101, FALSE, '1.0', 'Debian', 'VM', '4vCPU', '8GB', NULL),
(20002, 'FranchiseB', NULL, '10.10.1.2', '192.168.10.2', 'connectee', NOW(), NULL, 1010102, FALSE, '1.0', 'Debian', 'VM', '4vCPU', '8GB', NULL);

-- instance par client final 
INSERT INTO Instance (Num_Serie, Nom, RetourMateriel, AdresseIP, AdresseIP_VPN, Etat, DateInstallation, DatePeremption, NumeroLicence, MaterielRecupere, VersionApp, VersionOS, TypeMateriel, CPU, RAM, Id_ClientFinal)
VALUES
(10010, 'AlphaA-01', NULL, '10.2.1.1', '192.168.2.1', 'connectee', NOW(), NULL, 11001, FALSE, '1.1', 'Ubuntu', 'Raspberry', '2vCPU', '4GB', 1),
(10011, 'AlphaB-01', NULL, '10.2.1.2', '192.168.2.2', 'connectee', NOW(), NULL, 11002, FALSE, '1.1', 'Ubuntu', 'Raspberry', '2vCPU', '4GB', 2),
(10012, 'BetaA-01', NULL, '10.3.1.1', '192.168.3.1', 'connectee', NOW(), NULL, 12001, FALSE, '1.1', 'Debian', 'VM', '2vCPU', '2GB', 3),
(10013, 'BetaB-01', NULL, '10.3.1.2', '192.168.3.2', 'deconnectee', NOW(), NULL, 12002, FALSE, '1.1', 'Debian', 'VM', '2vCPU', '2GB', 4),
(10014, 'GammaA-01', NULL, '10.4.1.1', '192.168.4.1', 'connectee', NOW(), NULL, 13001, FALSE, '1.2', 'Alpine', 'Raspberry', '4vCPU', '8GB', 5),
(10015, 'GammaB-01', NULL, '10.4.1.2', '192.168.4.2', 'connectee', NOW(), NULL, 13002, FALSE, '1.2', 'Alpine', 'Raspberry', '4vCPU', '8GB', 6),
(10016, 'DeltaA-01', NULL, '10.5.1.1', '192.168.5.1', 'connectee', NOW(), NULL, 14001, FALSE, '1.0', 'Debian', 'VM', '2vCPU', '4GB', 7),
(10017, 'DeltaB-01', NULL, '10.5.1.2', '192.168.5.2', 'connectee', NOW(), NULL, 14002, TRUE, '1.0', 'Debian', 'VM', '2vCPU', '4GB', 8),  -- Matériel à récupérer
(10018, 'EpsilonA-01', NULL, '10.6.1.1', '192.168.6.1', 'connectee', NOW(), NULL, 15001, FALSE, '1.3', 'Ubuntu', 'VM', '1vCPU', '1GB', 9),
(10019, 'EpsilonB-01', NULL, '10.6.1.2', '192.168.6.2', 'connectee', NOW(), NULL, 15002, FALSE, '1.3', 'Ubuntu', 'VM', '1vCPU', '1GB', 10);


-- 5. Incidents (2 instances différentes) --
INSERT INTO Incident (Motif, DateIncident, Id_Tech, Num_Serie, Nom)
VALUES
('Panne réseau', NOW(), 1, 10010, 'AlphaA-01'),     -- sur la première instance
('Erreur disque', NOW(), 2, 10013, 'BetaB-01');     -- sur une autre instance



-- 6. Redemarrages --
INSERT INTO Redemarrage (Motif, DateRedemarrage, Num_Serie, Nom, Id_Tech)
VALUES
('Redémarrage manuel pour mise à jour', NOW(), 10010, 'AlphaA-01', 1),
('Redémarrage suite incident disque', NOW(), 10013, 'BetaB-01', 2);


-- 7. ScriptInstall -- 
INSERT INTO ScriptInstalle (NomScript, VersionScript) VALUES
('ScriptA', '1.0'),
('ScriptB', '2.1');


-- 8. Installation --
INSERT INTO Installation (Num_Serie, Nom, Id_Script, DateInstal)
VALUES
(10010, 'AlphaA-01', 1, NOW()),
(10013, 'BetaB-01', 2, NOW());


-- 9. Disque --
INSERT INTO Disques (TypeDisque, TailleDisque, Num_Serie, Nom)
VALUES
('SSD', 256, 10010, 'AlphaA-01'),
('HDD', 512, 10013, 'BetaB-01');
