from flask import Blueprint, render_template
from app.database import get_db_connection

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/')
def stats_home():
    return render_template('tables.html')

@stats_bp.route('/tables')
def view_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all tables
    cursor.execute('SELECT * FROM tables')
    tables = cursor.fetchall()
    conn.close()
    return render_template('tables.html', tables=tables)

@stats_bp.route('/tables/<int:table_id>')
def view_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch table metadata
    cursor.execute('SELECT * FROM tables WHERE id = ?', (table_id,))
    table = cursor.fetchone()

    # Fetch rows for the table
    cursor.execute('SELECT * FROM rows WHERE table_id = ?', (table_id,))
    rows = cursor.fetchall()

    conn.close()
    return render_template('table_view.html', table=table, rows=rows)