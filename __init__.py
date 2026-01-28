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

################################      Auth client      ##################################
# Route pour l'authentification des clients (Lecteurs)
@app.route('/authentification_client', methods=['GET', 'POST'])
def authentification_client():
    if request.method == 'POST':
        # Identifiants pour le client (Tu pourras plus tard remplacer ça par une vérif BDD)
        user = request.form['username']
        mdp = request.form['password']

        # On vérifie si c'est le bon client
        if user == 'client' and mdp == 'client123':
            # On active la session "authentifie" (celle utilisée par ta fonction est_authentifie)
            session['authentifie'] = True
            session['user_name'] = user
            # --- LA DEMANDE : Redirection vers la consultation des livres ---
            return redirect(url_for('consultation_livres'))
        else:
            # En cas d'erreur
            return render_template('formulaire_client.html', error=True)

    # Affichage du formulaire si on est en GET
    return render_template('formulaire_client.html', error=False)
    ###########################################################################################
    ##########################       Emprunter              #####################################
@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    if not est_authentifie():
        return redirect(url_for('authentification_client'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 1. Vérif du stock
    cursor.execute('SELECT stock FROM livres WHERE id = ?', (id_livre,))
    resultat = cursor.fetchone()

    if resultat and resultat[0] > 0:
        # 2. On baisse le stock
        cursor.execute('UPDATE livres SET stock = stock - 1 WHERE id = ?', (id_livre,))
        
        # 3. --- NOUVEAU : On enregistre l'emprunt ---
        # On récupère le nom stocké dans la session (ou 'Inconnu' si bug)
        emprunteur = session.get('user_name', 'Inconnu')
        
        cursor.execute('INSERT INTO emprunts (livre_id, nom_emprunteur) VALUES (?, ?)', 
                       (id_livre, emprunteur))
        
        conn.commit()
    
    conn.close()
    return redirect(url_for('consultation_livres'))
    #########################################################################
######################## Emprunter en cours #################################
@app.route('/emprunts_en_cours')
def emprunts_en_cours():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Requete SQL intelligente : On joint les deux tables
    sql = """
        SELECT livres.titre, livres.auteur, emprunts.nom_emprunteur 
        FROM emprunts 
        INNER JOIN livres ON emprunts.livre_id = livres.id
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()

    return render_template('mes_emprunts.html', data=data)
     ########################################################################
# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/consultation_livres/')
def consultation_livres():
    # Connexion standard
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Indispensable pour utiliser row['titre']
    cursor = conn.cursor()
    
    # La requête propre : on interroge la table 'livres' (en français)
    # et on ne prend que ceux qui ont du stock
    cursor.execute('SELECT * FROM livres WHERE stock > 0;')
    
    data = cursor.fetchall()
    conn.close()
    
    return render_template('read_books.html', data=data)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    # (Optionnel) Ici, tu pourrais ajouter : if not est_admin_authentifie(): ...
    
    # --- CAS 1 : L'utilisateur a rempli le formulaire (POST) ---
    if request.method == 'POST':
        # 1. On récupère les infos tapées dans les champs
        titre = request.form['titre']
        auteur = request.form['auteur']
        stock = request.form['stock']

        # 2. Connexion BDD
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # 3. Requête d'ajout
        # On suppose que ta table s'appelle 'books' avec les colonnes title, author, stock
        cursor.execute('INSERT INTO books (title, author, stock) VALUES (?, ?, ?)', 
                       (titre, auteur, stock))
        
        conn.commit()
        conn.close()

        # 4. Une fois fini, on retourne à la liste des livres
        return redirect(url_for('consultation_livres'))

    # --- CAS 2 : L'utilisateur veut voir le formulaire (GET) ---
    return render_template('formulaire_livre.html')
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
