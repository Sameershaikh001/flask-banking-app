from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import User, Transaction
from .services import transfer_funds, deposit_funds, withdraw_funds
from .utils import admin_required

bp = Blueprint('main', __name__)

# ------------------------------------------------------------
# Frontend Pages (serve HTML)
# ------------------------------------------------------------
from flask import render_template

@bp.route('/')
def index():
    return render_template('login.html')   # or redirect to login

@bp.route('/login-page')
def login_page():
    return render_template('login.html')

@bp.route('/register-page')
def register_page():
    return render_template('register.html')

@bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@bp.route('/profile-page')
def profile_page():
    return render_template('profile.html')

@bp.route('/transactions-page')
def transactions_page():
    return render_template('transactions.html')

@bp.route('/transfer-page')
def transfer_page():
    return render_template('transfer.html')

@bp.route('/admin-page')
def admin_page():
    return render_template('admin.html')

# ------------------------------------------------------------
# Public endpoints
# ------------------------------------------------------------

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = user.generate_auth_token()
    return jsonify({'access_token': access_token}), 200

# ------------------------------------------------------------
# Protected endpoints (any authenticated user)
# ------------------------------------------------------------

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    try:
        user = User.query.get(int(current_user_id))
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'balance': user.balance,
        'role': user.role,                     # <-- NEW field
        'created_at': user.created_at
    }), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    try:
        user = User.query.get(int(current_user_id))
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Update email if provided
    if 'email' in data:
        new_email = data['email']
        # Check if email is already taken by another user
        existing = User.query.filter_by(email=new_email).first()
        if existing and existing.id != user.id:
            return jsonify({'message': 'Email already in use'}), 400
        user.email = new_email

    # Update password if provided
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@bp.route('/balance', methods=['GET'])
@jwt_required()
def balance():
    current_user_id = get_jwt_identity()
    try:
        user = User.query.get(int(current_user_id))
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'balance': user.balance}), 200

@bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    current_user_id = get_jwt_identity()
    try:
        sender_id = int(current_user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    data = request.get_json()
    receiver_username = data.get('to_username')
    amount = data.get('amount')
    description = data.get('description', '')

    if not receiver_username or not amount:
        return jsonify({'message': 'Missing to_username or amount'}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'message': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid amount'}), 400

    sender = User.query.get(sender_id)
    if not sender:
        return jsonify({'message': 'Sender not found'}), 404

    receiver = User.query.filter_by(username=receiver_username).first()
    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 404

    if sender.balance < amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    transaction = transfer_funds(sender, receiver, amount, description)
    if transaction:
        return jsonify({
            'message': 'Transfer successful',
            'transaction_id': transaction.id,
            'new_balance': sender.balance
        }), 200
    else:
        return jsonify({'message': 'Transfer failed due to internal error'}), 500

@bp.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    current_user_id = get_jwt_identity()
    try:
        user_id = int(current_user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10  # sensible limits

    # Combine sent and received transactions
    sent = Transaction.query.filter_by(sender_id=user.id)
    received = Transaction.query.filter_by(receiver_id=user.id)
    all_tx = sent.union(received).order_by(Transaction.timestamp.desc())
    paginated = all_tx.paginate(page=page, per_page=per_page, error_out=False)

    transactions_list = []
    for t in paginated.items:
        if t.sender_id == user.id:
            tx_type = 'sent'
            other = t.receiver.username
        else:
            tx_type = 'received'
            other = t.sender.username
        transactions_list.append({
            'id': t.id,
            'type': tx_type,
            ('to' if tx_type == 'sent' else 'from'): other,
            'amount': t.amount,
            'timestamp': t.timestamp,
            'description': t.description
        })

    return jsonify({
        'transactions': transactions_list,
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages
        }
    }), 200

# ------------------------------------------------------------
# Admin-only endpoints
# ------------------------------------------------------------

@bp.route('/deposit', methods=['POST'])
@jwt_required()
@admin_required
def deposit():
    current_user_id = get_jwt_identity()
    try:
        user_id = int(current_user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'message': 'Missing amount'}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'message': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid amount'}), 400

    new_balance = deposit_funds(user, amount)
    return jsonify({
        'message': 'Deposit successful',
        'new_balance': new_balance
    }), 200

@bp.route('/withdraw', methods=['POST'])
@jwt_required()
@admin_required
def withdraw():
    current_user_id = get_jwt_identity()
    try:
        user_id = int(current_user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user ID format'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'message': 'Missing amount'}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'message': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid amount'}), 400

    try:
        new_balance = withdraw_funds(user, amount)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({
        'message': 'Withdrawal successful',
        'new_balance': new_balance
    }), 200