import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import User
from app import db

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='web').first()
    if not user:
        admin = User(username='web', email='web@example.com', role='admin')
        admin.set_password('webpass')
        db.session.add(admin)
        db.session.commit()
        print("Admin user 'web' created.")
    else:
        print("Admin user 'web' already exists.")