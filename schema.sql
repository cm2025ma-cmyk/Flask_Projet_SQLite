DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS livres;
DROP TABLE IF EXISTS emprunts;
DROP TABLE IF EXISTS taches;

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    adresse TEXT NOT NULL
);

-- Voici la nouvelle table demandée
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL,
    nom_emprunteur TEXT NOT NULL,
    FOREIGN KEY (livre_id) REFERENCES livres (id)
);

CREATE TABLE taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description VARCHAR(300),
    date_echeance DATE,
    etat BOOLEAN DEFAULT 0
);
