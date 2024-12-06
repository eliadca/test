from flask import Blueprint, render_template

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/')
def stats_home():
    return render_template('stats.html')

@stats_bp.route('/content')
def stats_content():
    return "<h2>Estadísticas Content</h2><p>Here you can manage statistics.</p>"