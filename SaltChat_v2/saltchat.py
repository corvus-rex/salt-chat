from flask import Flask, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.Integer, nullable=False)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        loginUsername = request.form['username']
        loginPassword = request.form['userpassword']
        login(loginUsername,loginPassword)
    else:
        return render_template('login.html')

def login(username,password):
    user = Users.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return render_template('login.html', error="Incorrect credentials. Please try again.")
    else:
        pass

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)