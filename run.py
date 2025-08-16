from flask import Flask
from app.routes.routes import routes_bp
import psycopg2
import sys
import os
sys.path.append(os.path.abspath("app"))

from app.database.models.models import db, User

app = Flask(__name__)

# Configuration clé secrète
app.config["SECRET_KEY"] = "9f2d1b7c6a8e5d9a3f4b2c7e9d0f1a3b"
app.config["SESSION_COOKIE_NAME"] = "metacollect_session"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.register_blueprint(routes_bp)  


DB_NAME = "metacollect"
DB_USER = "postgres"        
DB_PASSWORD = "Faly"  
DB_HOST = "localhost"
DB_PORT = "5432"

# Créer la base de données si elle n'existe pas
try:
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Base {DB_NAME} créée")
    cursor.close()
    conn.close()
except Exception as e:
    print("Erreur lors de la création de la base:", e)


app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()
    print("Tables créées ou déjà existantes")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
