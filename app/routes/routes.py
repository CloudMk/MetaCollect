from flask import Blueprint, render_template

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/')
def welcome():
    return render_template('view/welcome.html')

@routes_bp.route('/auth')
def index():
    return render_template('view/auth.html')
