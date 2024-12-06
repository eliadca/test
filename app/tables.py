from flask import Blueprint, jsonify, request
from app.database import get_db_connection

tables_bp = Blueprint('tables', __name__, url_prefix='/tables')

@tables_bp.route('/', methods=['GET'])
def get_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tables')
    tables = cursor.fetchall()
    conn.close()
    return jsonify(tables)

@tables_bp.route('/add', methods=['POST'])
def add_table():
    data = request.get_json()
    title = data.get('title')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tables (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Table added successfully'})

@tables_bp.route('/<int:table_id>/add_row', methods=['POST'])
def add_row(table_id):
    data = request.get_json()
    name = data.get('name', '')
    ab = data.get('ab', 0)
    h = data.get('h', 0)
    k = data.get('k', 0)
    bb = data.get('bb', 0)
    hbp = data.get('hbp', 0)
    doubles = data.get('doubles', 0)
    triples = data.get('triples', 0)
    hr = data.get('hr', 0)
    rbi = data.get('rbi', 0)
    r = data.get('r', 0)

    ave = h / ab if ab > 0 else 0
    ops = ave + bb / (ab + bb) if (ab + bb) > 0 else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO rows (table_id, name, ave, ab, h, k, bb, hbp, doubles, triples, hr, rbi, r, ops)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (table_id, name, ave, ab, h, k, bb, hbp, doubles, triples, hr, rbi, r, ops))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Row added successfully'})

@tables_bp.route('/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Table deleted successfully'})