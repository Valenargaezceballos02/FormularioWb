import pyotp

otp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
print('Código 2FA actual: ', otp.now())
