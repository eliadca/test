from flask import Blueprint, jsonify, request, render_template, Response 
from weasyprint import HTML
from app.database import get_db_connection

tables_bp = Blueprint('tables', __name__, url_prefix='/tables')

@tables_bp.route('/download/<int:table_id>', methods=['GET'])
def download_table_html_to_pdf(table_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the table title
    cursor.execute('SELECT title FROM tables WHERE id = ?', (table_id,))
    table = cursor.fetchone()
    if not table:
        return jsonify({'error': 'Table not found'}), 404

    title = table[0]

    # Fetch rows for the table
    cursor.execute('SELECT name, ave, ab, h, k, bb, hbp, doubles, triples, hr, rbi, r, ops FROM rows WHERE table_id = ?', (table_id,))
    rows = cursor.fetchall()
    conn.close()

    # Render the HTML content
    html_content = render_template('table_pdf.html', title=title, rows=rows)

    # Convert HTML to PDF with WeasyPrint
    pdf = HTML(string=html_content).write_pdf()

    # Return the PDF as a response
    return Response(pdf, mimetype='application/pdf', headers={"Content-Disposition": f"attachment; filename={title}.pdf"})

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

@tables_bp.route('/<int:table_id>', methods=['GET'])
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

@tables_bp.route('/<int:table_id>/delete_row/<int:row_id>', methods=['DELETE'])
def delete_row(table_id, row_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM rows WHERE id = ? AND table_id = ?', (row_id, table_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Row deleted successfully'})

@tables_bp.route('/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Table deleted successfully'})

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
