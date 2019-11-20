from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)
onlineUsers = []
onlineUserAvatars = []
app.secret_key = os.urandom(24)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.Integer)

@app.route('/')
def index():
    currentUser = session.get('username')
    if currentUser in onlineUsers:
    #connectionEvent()
        return redirect('/chat')
    else:
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

@app.route('/chat', methods=['POST', 'GET'])
def chatRoom():
    if request.referrer is None:
        return render_template('login.html')
    else:
        return render_template('chat.html')

def login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return "YOU SHALL NOT PASS!"
    else:
        updatesession(user)
        return redirect('/')

def register(username, password):
    if existingusername(username) == True:
        return "This username already exist!"
    else:
        newUser = Users(username=username, password=password)

        db.session.add(newUser)
        db.session.commit()
        updatesession(newUser)
        return redirect('/')

def existingusername(username):
    existingUsers = Users.query.filter_by(username=username).count()
    if existingUsers > 0:
        return True
    else:
        return False

def updatesession(user):
    session['username'] = user.username
    session['userid'] = user.id
    session['avatar'] = user.avatar
    onlineUsers.append(user.username)
    onlineUserAvatars.append(user.avatar)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)