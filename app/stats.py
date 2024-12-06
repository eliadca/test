from flask import Blueprint, render_template
from app.database import get_db_connection

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/')
def stats_home():
    return render_template('stats.html')

@stats_bp.route('/tables')
def stats_tables():
    return render_template('tables.html')
