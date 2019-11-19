from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)