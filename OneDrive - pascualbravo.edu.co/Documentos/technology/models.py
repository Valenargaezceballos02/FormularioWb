# from werkzeug.security import generate_password_hash

# users = {
#     'admin': {
#         'password': generate_password_hash('admin123'),
#         'role': 'admin',
#         'otp_secret': 'JBSWY3DPEHPK3PXP'
#     },
#     'operador': {
#         'password': generate_password_hash('user123'),
#         'role': 'user',
#         'otp_secret': 'JBSWY3DPEHPK3PXG'
#     }
# }


from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import secrets
import random
import string


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='user')
    otp_secret_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = sha256_crypt.hash(password)

    def set_otp_secret(self):
        caracteres = string.ascii_letters + string.digits
        texto = ''.join(random.choices(caracteres, k=10))
        print(texto)
        #otp = secrets.token_hex().capitalize()  # genera 10 caracteres
        self.otp_secret_hash = texto

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "username": self.username,
            "rol": self.rol,
            "otp_secret_hash": self.otp_secret_hash,
            "password": self.password_hash
        }

