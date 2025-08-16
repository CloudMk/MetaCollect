from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import ici pour éviter les imports circulaires
    from app.routes.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
