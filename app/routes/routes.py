from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
import random
import smtplib  # pour envoyer email
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor

routes_bp = Blueprint('routes_bp', __name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        dbname="metacollect",
        user="postgres",
        password="Faly"
    )
    return conn


# ----------------------
# PAGE D'ACCUEIL
# ----------------------
@routes_bp.route('/')
def welcome():
    return render_template('view/welcome.html')


# ----------------------
# ENVOI CODE PAR MAIL
# ----------------------
@routes_bp.route("/send-code", methods=["POST"])
def send_code():
    email = request.json.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email manquant"}), 400

    code = str(random.randint(100000, 999999))

    try:
        sender_email = "faliarisoazafindrasojacharlotr@gmail.com"
        app_password = "obcw hqqn ucuc uiuy"  # mot de passe d'application Gmail

        message = MIMEText(f"Votre code de confirmation est : {code}")
        message["Subject"] = "Code de confirmation DataCollect"
        message["From"] = sender_email
        message["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email, message.as_string())

        print(f"Code envoyé à {email} : {code}")

        session["confirmation_code"] = code
        session["confirmation_email"] = email

        return jsonify({"success": True, "message": "Code envoyé"})
    
    except Exception as e:
        print("Erreur email:", e)
        return jsonify({"success": False, "message": "Impossible d'envoyer le code"}), 500


# ----------------------
# INSCRIPTION
# ----------------------
@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("view/register.html")

    username = request.form.get("nom")
    email = request.form.get("email")
    password = request.form.get("passwd")
    profil = request.form.get("file")
    confirmation_code = request.form.get("confirmation_code")

    if not username or not email or not password or not confirmation_code:
        flash("Veuillez remplir tous les champs", "danger")
        return redirect(url_for("routes_bp.register"))

    saved_code = session.get("confirmation_code")
    saved_email = session.get("confirmation_email")

    if not saved_code or not saved_email:
        flash("Veuillez d'abord demander un code de confirmation", "warning")
        return redirect(url_for("routes_bp.register"))

    if confirmation_code != saved_code or email != saved_email:
        flash("Code de confirmation invalide", "danger")
        return redirect(url_for("routes_bp.register"))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        flash("Un compte avec cet email existe déjà", "warning")
        cur.close()
        conn.close()
        return redirect(url_for("routes_bp.login"))

    hashed_password = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (nom, email, passwd, profil) VALUES (%s, %s, %s, %s) RETURNING id",
        (username, email, hashed_password, profil)
    )
    conn.commit()
    cur.close()
    conn.close()

    session.pop("confirmation_code", None)
    session.pop("confirmation_email", None)

    flash("Compte créé avec succès, veuillez vous connecter", "success")
    return redirect(url_for("routes_bp.login"))


# ----------------------
# CONNEXION
# ----------------------
@routes_bp.route("/login", methods=["GET", "POST"])@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("routes_bp.accueil"))
        return render_template("view/welcome.html")  # page login
    else:
        # POST : traitement du formulaire
        email = request.form.get("email")
        password = request.form.get("passwd")

        if not email or not password:
            flash("Veuillez entrer votre email et votre mot de passe", "danger")
            return redirect(url_for("routes_bp.login"))

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            flash("Aucun compte trouvé avec cet email. Veuillez créer un compte.", "warning")
            return redirect(url_for("routes_bp.register"))

        if not check_password_hash(user["passwd"], password):
            flash("Mot de passe incorrect", "danger")
            return redirect(url_for("routes_bp.login"))

        # Stocker les infos en session
        session["user_id"] = user["id"]
        session["nom"] = user["nom"]

        flash(f"Bienvenue {user['nom']} !", "success")
        return redirect(url_for("routes_bp.accueil"))



# ----------------------
# PAGE ACCUEIL APRÈS LOGIN
# ----------------------
@routes_bp.route("/accueil")
def accueil():
    if "user_id" not in session:
        flash("Veuillez vous connecter pour accéder à l'accueil", "warning")
        return redirect(url_for("routes_bp.login"))
    return render_template("view/accueil.html", username=session.get("nom"))


# ----------------------
# DÉCONNEXION
# ----------------------
@routes_bp.route("/logout")
def logout():
    session.clear()
    flash("Vous avez été déconnecté. Veuillez vous reconnecter.", "info")
    return redirect(url_for("routes_bp.login"))


# ----------------------
# CRÉATION PROJET
# ----------------------
projets = []

@routes_bp.route("/nouveau-projet", methods=["GET", "POST"])
def nouveau_projet():
    if "user_id" not in session:
        flash("Veuillez vous connecter pour créer un projet", "warning")
        return redirect(url_for("routes_bp.login"))

    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description")
        if titre and description:
            projet = {"titre": titre, "description": description, "auteur": session["nom"]}
            projets.append(projet)
            flash("Projet créé avec succès !", "success")
            return redirect(url_for("routes_bp.accueil"))
        else:
            flash("Veuillez remplir tous les champs", "danger")

    return render_template("view/creat_projet.html")
