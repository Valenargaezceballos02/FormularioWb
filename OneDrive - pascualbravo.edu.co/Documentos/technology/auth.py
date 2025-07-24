# from flask_login import LoginManager, UserMixin
# #from models import users

# login_manager = LoginManager()
# login_manager.login_view = 'login'

# class AuthUser(UserMixin):
#     def __init__(self, user):
#         self.id = user.id
#         self.username = user.username

# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return AuthUser(user) if user else None
