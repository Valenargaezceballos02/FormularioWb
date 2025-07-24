import pyotp

otp = pyotp.TOTP('KKIeqWvnmG')
print('Código 2FA actual: ', otp.now())
