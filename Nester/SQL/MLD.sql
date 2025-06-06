-- Table Prestataire
CREATE TABLE Prestataire (
    SIRET INT PRIMARY KEY,
    Nom VARCHAR(45) NOT NULL,
    Adresse VARCHAR(45) NOT NULL,
    Contact VARCHAR(45) NOT NULL
);

-- Table Client_Final
CREATE TABLE Client_Final (
    Id_ClientFinal SERIAL PRIMARY KEY,
    Nom VARCHAR(45) NOT NULL,
    Adresse VARCHAR(45) NOT NULL,
    SIRET INT REFERENCES Prestataire(SIRET)
);

-- Table Technicien
CREATE TABLE Technicien (
    Id_Tech SERIAL PRIMARY KEY,
    Nom VARCHAR(45) NOT NULL,
    Role VARCHAR(45) NOT NULL
);

-- Table Instance 
CREATE TABLE Instance (
    Num_Serie INT,
    Nom VARCHAR(45),
    RetourMateriel VARCHAR(50),
    AdresseIP VARCHAR(16) NOT NULL,
    AdresseIP_VPN VARCHAR(16) NOT NULL,
    Etat VARCHAR(25) NOT NULL,
    DateInstallation TIMESTAMP NOT NULL,
    DatePeremption TIMESTAMP,
    NumeroLicence INT NOT NULL,
    MaterielRecupere BOOLEAN NOT NULL,
    VersionApp VARCHAR(10) NOT NULL,
    VersionOS VARCHAR(30) NOT NULL,
    TypeMateriel VARCHAR(30) NOT NULL,
    CPU VARCHAR(40) NOT NULL,
    RAM VARCHAR(30) NOT NULL,
    Id_ClientFinal INT NOT NULL,
    PRIMARY KEY(Num_Serie, Nom),
    FOREIGN KEY(Id_ClientFinal) REFERENCES Client_Final(Id_ClientFinal)
);

-- Table Incident
CREATE TABLE Incident (
    Id_Incident SERIAL PRIMARY KEY,
    Motif TEXT NOT NULL,
    DateIncident TIMESTAMP NOT NULL,
    Id_Tech INT NOT NULL,
    Num_Serie INT NOT NULL,
    Nom VARCHAR(45) NOT NULL,
    FOREIGN KEY(Id_Tech) REFERENCES Technicien(Id_Tech),
    FOREIGN KEY(Num_Serie, Nom) REFERENCES Instance(Num_Serie, Nom)
);

-- Table ScriptInstalle
CREATE TABLE ScriptInstalle (
    Id_Script SERIAL PRIMARY KEY,
    NomScript VARCHAR(45) NOT NULL,
    VersionScript VARCHAR(40) NOT NULL
);

-- Table Redemarrage
CREATE TABLE Redemarrage (
    Id_Redemarrage SERIAL PRIMARY KEY,
    Motif TEXT NOT NULL,
    DateRedemarrage TIMESTAMP NOT NULL,
    Num_Serie INT NOT NULL,
    Nom VARCHAR(45) NOT NULL,
    Id_Tech INT NOT NULL,
    FOREIGN KEY(Num_Serie, Nom) REFERENCES Instance(Num_Serie, Nom),
    FOREIGN KEY(Id_Tech) REFERENCES Technicien(Id_Tech)
);

-- Table Disques
CREATE TABLE Disques (
    Id_Disque SERIAL PRIMARY KEY,
    TypeDisque VARCHAR(50) NOT NULL,
    TailleDisque INT NOT NULL,
    Num_Serie INT,
    Nom VARCHAR(45),
    FOREIGN KEY(Num_Serie, Nom) REFERENCES Instance(Num_Serie, Nom)
);

-- Table Installation
CREATE TABLE Installation (
    Num_Serie INT,
    Nom VARCHAR(45),
    Id_Script INT,
    DateInstal TIMESTAMP NOT NULL,
    PRIMARY KEY(Num_Serie, Nom, Id_Script),
    FOREIGN KEY(Num_Serie, Nom) REFERENCES Instance(Num_Serie, Nom),
    FOREIGN KEY(Id_Script) REFERENCES ScriptInstalle(Id_Script)
);
