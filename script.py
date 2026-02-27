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