from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from .models import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        try:
            user = User.query.get(int(current_user_id))
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid user'}), 401
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function