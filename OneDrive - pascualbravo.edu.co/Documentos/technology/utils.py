from functools import wraps
from flask import redirect, url_for, render_template
from flask_login import current_user
import logging

# Configuración de auditoría
logging.basicConfig(filename='audit.log', level=logging.INFO)

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.role != role:
                logging.warning(f"ACCESO DENEGADO: {current_user.id} intentó acceder a una ruta restringida ({role})")
                return render_template('access_denied.html')
            return f(*args, **kwargs)
        return decorated
    return wrapper

def log_event(message):
    logging.info(message)

