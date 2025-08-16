from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    passwd = db.Column(db.String(300), nullable=False)
    profil = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<User {self.nom}>"

