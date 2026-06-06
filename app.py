from flask import Flask, render_template
from models import db

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
app.config['SECRET_KEY'] = 'vendorbridge_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorbridge.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -----------------------------
# Initialize Database
# -----------------------------
db.init_app(app)

# -----------------------------
# Home / Dashboard Route
# -----------------------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# -----------------------------
# Create Database Tables
# -----------------------------
with app.app_context():
    db.create_all()


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )