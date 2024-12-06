from flask import Blueprint, render_template

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/')
def stats_home():
    return render_template('stats.html')