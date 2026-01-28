from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

######Bilibothèque#######################
# Fonction pour vérifier si c'est un admin
def est_admin_authentifie():
    return session.get('admin_authentifie')

@app.route('/admin')
def admin_panel():
    if not est_admin_authentifie():
        # Si pas admin, on renvoie vers le login admin
        return redirect(url_for('authentification_admin'))
    
    return "<h2>Bienvenue dans l'espace Administrateur (Gestion Stocks & Utilisateurs)</h2>"

@app.route('/authentification_admin', methods=['GET', 'POST'])
def authentification_admin():
    if request.method == 'POST':
        # Vérifier les identifiants SPÉCIFIQUES à l'admin
        # Ici on utilise 'admin' et 'admin123'
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin_authentifie'] = True
            # Rediriger vers le panneau admin après succès
            return redirect(url_for('admin_panel'))
        else:
            # Erreur d'authentification
            return render_template('formulaire_admin.html', error=True)

    return render_template('formulaire_admin.html', error=False)
# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/consultation_livres/')
def consultation_livres():
    conn = sqlite3.connect('database.db')
    
    # Cette ligne est très utile : elle permet de récupérer les données par nom de colonne
    conn.row_factory = sqlite3.Row 
    
    cursor = conn.cursor()
    
    # --- LA PARTIE IMPORTANTE ---
    # On sélectionne tous les livres dont le stock est strictement supérieur à 0
    cursor.execute('SELECT * FROM livres;')
    
    data = cursor.fetchall()
    conn.close()
    
    # On envoie les données vers une page HTML dédiée
    return render_template('read_books.html', data=data)
    #############################################################################

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/fiche_nom/<string:nom>')
def ReadficheByNom(nom):
    # --- 1. SÉCURITÉ (On vérifie d'abord) ---
    if not est_authentifie():
        # Si pas connecté -> Hop, direction la page de login
        return redirect(url_for('authentification'))

    # --- 2. RECHERCHE (Seulement si on est connecté) ---
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    data = cursor.fetchall()
    
    conn.close()
    
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
