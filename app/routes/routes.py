from flask import Blueprint, render_template, request, jsonify,session, redirect, url_for, flash
import random
import smtplib  # pour envoyer email (ou utiliser une API comme SendGrid)
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.models.models import db, User


routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/')
def welcome():
    return render_template('view/welcome.html')

@routes_bp.route('/auth')
def index():
    return render_template('view/auth.html')

@routes_bp.route("/send-code", methods=["POST"])
def send_code():
    email = request.json.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email manquant"}), 400

    # Générer un code à 6 chiffres
    code = str(random.randint(100000, 999999))

    try:
        # ⚠️ Remplace par ton vrai email et mot de passe d'application
        sender_email = "faliarisoazafindrasojacharlotr@gmail.com"
        app_password = "obcw hqqn ucuc uiuy"  # mot de passe d'application Gmail

        message = MIMEText(f"Votre code de confirmation est : {code}")
        message["Subject"] = "Code de confirmation DataCollect"
        message["From"] = sender_email
        message["To"] = email

        # Connexion SMTP Gmail sécurisée
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, email, message.as_string())

        # Pour test console
        print(f"Code envoyé à {email} : {code}")

        # Ici tu peux sauvegarder le code en session ou base de données pour vérification
        return jsonify({"success": True, "message": "Code envoyé", "code": code})
    
    except smtplib.SMTPAuthenticationError:
        print("Erreur email: identifiants incorrects ou mot de passe d'application manquant")
        return jsonify({"success": False, "message": "Erreur d'authentification email"}), 500
    except Exception as e:
        print("Erreur email:", e)
        return jsonify({"success": False, "message": "Impossible d'envoyer le code"}), 500

# Inscription utilisateur et stockage en PostgreSQL
@routes_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation_code = request.form.get("confirmation_code")
    file = request.files.get("file")

    saved_code = session.get("confirmation_code")
    saved_email = session.get("confirmation_email")

    # Vérification du code de confirmation
    if not saved_code or email != saved_email or confirmation_code != saved_code:
        flash("Code de confirmation invalide", "danger")
        return redirect(url_for("routes_bp.index"))

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(email=email).first():
        flash("Email déjà utilisé", "danger")
        return redirect(url_for("routes_bp.login"))

    # Hacher le mot de passe
    hashed_pass = generate_password_hash(password)

    # Insertion directe via SQL dans PostgreSQL
    from sqlalchemy import text
    sql = text(
        "INSERT INTO users (nom, email, passwd, profil) VALUES (:nom, :email, :passwd, :profil)"
    )
    db.session.execute(sql, {"nom": username, "email": email, "passwd": hashed_pass, "profil": "Utilisateur standard"})
    db.session.commit()

    # Supprimer le code de session après inscription réussie
    session.pop("confirmation_code", None)
    session.pop("confirmation_email", None)

    flash(f"Utilisateur {username} créé avec succès !", "success")
    
@routes_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("view/accueil.html")

@routes_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.passwd, password):
        session["user"] = {"nom": user.nom, "email": user.email}
        flash("Connexion réussie, bienvenue !", "success")
        return redirect(url_for("routes_bp.accueil"))
    else:
        flash("Email ou mot de passe incorrect", "danger")
        return redirect(url_for("routes_bp.login_page"))

# Déconnexion
@routes_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("routes_bp.welcome"))

@routes_bp.route("/accueil")
def accueil():
    if "users" not in session:
        flash("Veuillez vous connecter pour accéder à l'accueil", "warning")
        return redirect(url_for("routes_bp.login"))
    
    user = session.get("users")  
    
    return render_template("view/accueil.html", user=user)

projets = []

@routes_bp.route("/nouveau-projet", methods=["GET", "POST"])
def nouveau_projet():
    if request.method == "POST":
        titre = request.form.get("titre")
        description = request.form.get("description")
        if titre and description:
            projet = {"titre": titre, "description": description, "auteur": session["user"]}
            projets.append(projet)
            flash("Projet créé avec succès !", "success")
            return redirect(url_for("routes_bp.accueil"))
        else:
            flash("Veuillez remplir tous les champs", "danger")

    return render_template("view/creat_projet.html")


