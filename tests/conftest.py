import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

load_dotenv()

# ---------- API Fixture ----------
@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:5000"

@pytest.fixture
def api_client(base_url):
    def _api_client(endpoint, method="GET", data=None, token=None):
        url = base_url + endpoint
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = requests.request(method, url, json=data, headers=headers)
        return response
    return _api_client

@pytest.fixture
def auth_token(api_client):
    # Register a temporary user (ignore if exists)
    api_client("/register", "POST", {"username": "testuser", "email": "test@example.com", "password": "testpass"})
    resp = api_client("/login", "POST", {"username": "testuser", "password": "testpass"})
    token = resp.json().get("access_token")
    return token

# ---------- Selenium Fixture ----------
@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    #options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove to see browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ---------- Database Fixture (Fixed) ----------
@pytest.fixture(scope="function")
def db_session():
    """Provides a database session that rolls back after test using Flask's db.session."""
    from app import create_app
    from app.models import db as _db

    app = create_app()
    with app.app_context():
        # Start a transaction
        connection = _db.engine.connect()
        transaction = connection.begin()
        # Bind the Flask-SQLAlchemy session to this connection
        _db.session.remove()
        _db.session.configure(bind=connection)
        yield _db.session
        # Rollback and cleanup
        transaction.rollback()
        connection.close()
        _db.session.remove()
        _db.session.configure(bind=_db.engine)  # restore default binding