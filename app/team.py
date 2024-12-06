from flask import Blueprint

team_bp = Blueprint('team', __name__, url_prefix='/team')

@team_bp.route('/content')
def team_content():
    return "<h2>Equipo Content</h2><p>Here you can manage the team.</p>"