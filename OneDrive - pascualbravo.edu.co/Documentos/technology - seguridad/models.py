from werkzeug.security import generate_password_hash

users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin',
        'otp_secret': 'JBSWY3DPEHPK3PXP'
    },
    'operador': {
        'password': generate_password_hash('user123'),
        'role': 'user',
        'otp_secret': 'JBSWY3DPEHPK3PXG'
    }
}
