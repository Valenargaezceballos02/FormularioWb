from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pyotp
from werkzeug.security import check_password_hash
from datetime import timedelta

from config import SECRET_KEY, SESSION_DURATION_MINUTES
from models import users
from auth import login_manager, User
from utils import role_required, log_event

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=SESSION_DURATION_MINUTES)

login_manager.init_app(app)

@app.route('/', methods=['GET'])
def home():
     return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username]['password'], password):
            session['pre_2fa_user'] = username
            log_event(f"Usuario {username} pasó autenticación inicial.")
            return redirect('/2fa')
        log_event(f"Fallo de login para usuario: {username}")
    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    user = session.get('pre_2fa_user')
    if not user:
        return redirect('/')
    
    otp = pyotp.TOTP(users[user]['otp_secret'])

    if request.method == 'POST':
        code = request.form['code']
        if otp.verify(code):
            login_user(User(user))
            session.permanent = True
            log_event(f"Autenticación 2FA exitosa para {user}")
            return redirect('/dashboard')
        log_event(f"Fallo en 2FA para {user}")
    return render_template('2fa.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html', user=current_user)

@app.route('/user')
@login_required
@role_required('user')
def user():
    return render_template('user.html', user=current_user)

@app.route('/')
@login_required
def logout():
    log_event(f"Usuario {current_user.id} cerró sesión.")
    logout_user()
    return redirect('/templates/home.html')
    
if __name__ == '__main__':
    app.run(debug=True)
