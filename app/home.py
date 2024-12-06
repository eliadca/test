from flask import Flask, render_template
from .stats import stats_bp
from .tables import tables_bp

app = Flask(__name__)
app.register_blueprint(stats_bp)
app.register_blueprint(tables_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)