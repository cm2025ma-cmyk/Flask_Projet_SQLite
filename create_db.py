import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris'))

# --- INSERTION DES LIVRES (Nouveau code) ---
# Note : On insère le titre, l'auteur et le stock
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', 5))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('1984', 'George Orwell', 3))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Harry Potter à l''école des sorciers', 'J.K. Rowling', 4))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Les Misérables', 'Victor Hugo', 2))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('L''Étranger', 'Albert Camus', 0))

# ICI c'est l'appplication WEB task   #

# Tâche 1 : Non terminée (état = 0 ou False)
cur.execute("INSERT INTO taches (titre, description, date_echeance, etat) VALUES (?, ?, ?, ?)",
            ('Projet NFP107', 'Faire une app web', '2026-18-02', 0))

# Tâche 2 : Terminée (état = 1 ou True)
cur.execute("INSERT INTO taches (titre, description, date_echeance, etat) VALUES (?, ?, ?, ?)",
            ('Apprendre Flask', 'Suivre le tutoriel pour créer le gestionnaire de tâches.', '2025-10-25', 1))

connection.commit()
connection.close()
print("Base de données initialisée avec Clients et Livres et Emprunts !")
print("Base de données initialisée avec task !")

