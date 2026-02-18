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
        return redirect(url_for('authentification_admin'))
    return "<h2>Bienvenue dans l'espace Administrateur (Gestion Stocks & Utilisateurs)</h2>"

@app.route('/authentification_admin', methods=['GET', 'POST'])
def authentification_admin():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin_authentifie'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('formulaire_admin.html', error=True)
    return render_template('formulaire_admin.html', error=False)

################################      Auth client      ##################################
@app.route('/authentification_client', methods=['GET', 'POST'])
def authentification_client():
    if request.method == 'POST':
        user = request.form['username']
        mdp = request.form['password']
        if user == 'client' and mdp == 'client123':
            session['authentifie'] = True
            session['user_name'] = user
            return redirect(url_for('consultation_livres'))
        else:
            return render_template('formulaire_client.html', error=True)
    return render_template('formulaire_client.html', error=False)

###########################################################################################
@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    if not est_authentifie():
        return redirect(url_for('authentification_client'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM livres WHERE id = ?', (id_livre,))
    resultat = cursor.fetchone()
    if resultat and resultat[0] > 0:
        cursor.execute('UPDATE livres SET stock = stock - 1 WHERE id = ?', (id_livre,))
        emprunteur = session.get('user_name', 'Inconnu')
        cursor.execute('INSERT INTO emprunts (livre_id, nom_emprunteur) VALUES (?, ?)', 
                       (id_livre, emprunteur))
        conn.commit()
    conn.close()
    return redirect(url_for('consultation_livres'))

@app.route('/emprunts_en_cours')
def emprunts_en_cours():
    return "Page en construction"

def est_authentifie():
    return session.get('authentifie')

@app.route('/consultation_livres/')
def consultation_livres():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE stock > 0;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_books.html', data=data)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        stock = request.form['stock']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, stock) VALUES (?, ?, ?)', 
                       (titre, auteur, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('consultation_livres'))
    return render_template('formulaire_livre.html')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'user' and request.form['password'] == '12345':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/fiche_nom/<string:nom>')
def ReadficheByNom(nom):
    if not est_authentifie():
        return redirect(url_for('authentification'))
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
    return render_template('formulaire.html')

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

###################################################################################
#                       MINI PROJET GESTION DE TACHES                             #
###################################################################################

# 1. Page principale : Liste + Formulaire d'ajout
@app.route('/taches', methods=['GET', 'POST'])
def taches():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    if request.method == 'POST':
        # On ajoute la tâche
        titre = request.form['titre']
        description = request.form['description']
        date_echeance = request.form['date_echeance']
        
        cursor.execute("INSERT INTO taches (titre, description, date_echeance, etat) VALUES (?, ?, ?, 0)",
                       (titre, description, date_echeance))
        conn.commit()
        # Ici, on recharge simplement la même page pour voir l'ajout
        conn.close()
        return render_template('taches.html', taches=liste_taches)

    # Affichage de la liste
    cursor.execute("SELECT * FROM taches ORDER BY etat ASC, date_echeance ASC") 
    liste_taches = cursor.fetchall()
    conn.close()
    
    # On envoie les données au fichier taches.html
    return render_template('taches.html', taches=liste_taches)

@app.route('/changer_etat/<int:id>/<int:etat>')
def changer_etat(id, etat):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE taches SET etat = ? WHERE id = ?", (etat, id))
    conn.commit()
    conn.close()
    return render_template('taches.html', taches=liste_taches)

if __name__ == "__main__":
  app.run(debug=True)
