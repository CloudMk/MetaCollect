from flask import Flask
from app.routes.routes import routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp)  # pas de url_prefix pour que "/" marche

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)