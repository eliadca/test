from flask import Blueprint, jsonify, request
from app.database import get_db_connection

tables_bp = Blueprint('tables', __name__, url_prefix='/tables')

@tables_bp.route('/<int:table_id>/update_row/<int:row_id>', methods=['POST'])
def update_row(table_id, row_id):
    data = request.get_json()
    column = data.get('column')
    value = data.get('value')

    if column not in [
        'ab', 'h', 'k', 'bb', 'hbp', 'doubles', 'triples', 'hr', 'rbi', 'r'
    ]:
        return jsonify({'error': 'Invalid column name'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'UPDATE rows SET {column} = ? WHERE id = ? AND table_id = ?', (value, row_id, table_id))
    conn.commit()

    # Recalculate AVE and OPS after the update
    cursor.execute('SELECT ab, h, bb, hbp, doubles, triples, hr FROM rows WHERE id = ?', (row_id,))
    row = cursor.fetchone()
    ab, h, bb, hbp, doubles, triples, hr = row

    ave = h / ab if ab > 0 else 0
    obp = (h + bb + hbp) / (ab + bb + hbp) if (ab + bb + hbp) > 0 else 0
    slg = ((h - (doubles + triples + hr)) + (2 * doubles) + (3 * triples) + (4 * hr)) / ab if ab > 0 else 0
    ops = obp + slg

    cursor.execute('UPDATE rows SET ave = ?, ops = ? WHERE id = ?', (ave, ops, row_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Row updated successfully', 'ave': round(ave, 3), 'ops': round(ops, 3)})