from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.Integer)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def loginPage():
    if request.method == 'POST':
        loginUsername = request.form['username']
        loginPassword = request.form['password']
        return login(loginUsername, loginPassword)
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def registerPage():
    if request.method == 'POST':
        newUsername = request.form['username']
        newPassword = request.form['password']
        return register(newUsername, newPassword)
    else:
        return render_template('register.html')


def login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return "YOU SHALL NOT PASS!"
    else:
        return "You may enter the Kool Kids Klub"

def register(username, password):
    newUser = Users(username=username, password=password)
    try:
        db.session.add(newUser)
        db.session.commit()
        return redirect('/')
    except:
        return "Error in creating new user"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)