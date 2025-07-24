from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import pyotp
from werkzeug.security import check_password_hash
from datetime import timedelta
from models import db, User


from config import SECRET_KEY, SESSION_DURATION_MINUTES
#from models import users
#from auth import login_manager, User
from utils import role_required, log_event

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=SESSION_DURATION_MINUTES)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mock.db'
db.init_app(app)


#login_manager.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    # db.session.delete(User.query.filter_by(username='admin').first())
    # db.session.commit()

    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(

            nombre='Administrador',
            username='admin',
            rol='admin'
        )
        admin_user.set_password('admin123')
        admin_user.set_otp_secret()
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario admin precargado con éxito.")
    if not User.query.filter_by(username='user').first():
        admin_user = User(

            nombre='user',
            username='user',
            rol='user'
        )
        admin_user.set_password('user123')
        admin_user.set_otp_secret()
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario admin precargado con éxito.")


class AuthUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.role = user.rol

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return AuthUser(user) if user else None


@app.route('/', methods=['GET'])
def home():
     return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['pre_2fa_user'] = username
            login_user(AuthUser(user))
            log_event(f"Usuario {username} pasó autenticación inicial.")
            return redirect('/2fa')
        log_event(f"Fallo de login para usuario: {username}")
    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    user = session.get('pre_2fa_user')
    if not user:
        return redirect('/')
    user_db = User.query.filter_by(username=user).first()
    print(user_db.to_dict())
    otp = pyotp.TOTP(user_db.to_dict()['otp_secret_hash'])
    print('codigo:',otp.now())

    if request.method == 'POST':
        code = request.form['code']
        print(code)
        if otp.verify(code):
            login_user(AuthUser(user_db))
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
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
