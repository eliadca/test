from flask import Blueprint, jsonify, request, Response
from app.database import get_db_connection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Define Blueprint
tables_bp = Blueprint('tables', __name__, url_prefix='/tables')

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

@tables_bp.route('/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tables WHERE id = ?', (table_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Table deleted successfully'})

@tables_bp.route('/download/<int:table_id>', methods=['GET'])
def download_table(table_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch table title
    cursor.execute('SELECT title FROM tables WHERE id = ?', (table_id,))
    table = cursor.fetchone()
    if not table:
        return jsonify({'error': 'Table not found'}), 404

    title = table[0]

    # Fetch rows for the table
    cursor.execute('SELECT name, ave, ab, h, k, bb, hbp, doubles, triples, hr, rbi, r, ops FROM rows WHERE table_id = ?', (table_id,))
    rows = cursor.fetchall()
    conn.close()

    # Generate PDF
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Table - {title}")

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, f"Table: {title}")

    # Headers
    pdf.setFont("Helvetica-Bold", 12)
    headers = ["Name", "AVE", "AB", "H", "K", "BB", "HBP", "2B", "3B", "HR", "RBI", "R", "OPS"]
    x, y = 50, 720
    for header in headers:
        pdf.drawString(x, y, header)
        x += 50
    y -= 20

    # Rows
    pdf.setFont("Helvetica", 10)
    for row in rows:
        x = 50
        for col in row:
            pdf.drawString(x, y, str(col))
            x += 50
        y -= 20

        # Add new page if out of space
        if y < 50:
            pdf.showPage()
            y = 750

    pdf.save()

    # Return PDF as response
    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": f"attachment;filename={title}.pdf"})