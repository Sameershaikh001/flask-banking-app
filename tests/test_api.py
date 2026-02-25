import pytest
import uuid

def generate_unique_username(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def test_transfer_success(api_client, db_session):
    sender_username = generate_unique_username("sender")
    recipient_username = generate_unique_username("recipient")

    # Register sender and recipient
    api_client("/register", "POST", {
        "username": sender_username,
        "email": f"{sender_username}@test.com",
        "password": "pass123"
    })
    api_client("/register", "POST", {
        "username": recipient_username,
        "email": f"{recipient_username}@test.com",
        "password": "pass123"
    })

    # Login as sender to get token
    login_resp = api_client("/login", "POST", {"username": sender_username, "password": "pass123"})
    token = login_resp.json()["access_token"]

    # Retrieve sender and receiver from DB
    from app.models import User
    sender = db_session.query(User).filter_by(username=sender_username).first()
    receiver = db_session.query(User).filter_by(username=recipient_username).first()

    # Directly set sender balance
    sender.balance = 500
    db_session.commit()

    # Perform transfer
    resp = api_client("/transfer", "POST", {
        "to_username": recipient_username,
        "amount": 200
    }, token=token)

    print(f"Transfer response: {resp.status_code} - {resp.text}")
    assert resp.status_code == 200, f"Transfer failed: {resp.text}"
    data = resp.json()
    assert data["message"] == "Transfer successful"
    assert data["new_balance"] == 300

    # Refresh test session objects to see committed changes
    db_session.refresh(sender)
    db_session.refresh(receiver)

    # Verify in DB
    assert sender.balance == 300
    assert receiver.balance == 200

def test_transactions_pagination(api_client, db_session):
    from app.models import User, Transaction

    sender_username = generate_unique_username("sender")
    recipient_username = generate_unique_username("recipient")

    # Register via API
    api_client("/register", "POST", {
        "username": sender_username,
        "email": f"{sender_username}@test.com",
        "password": "pass123"
    })
    api_client("/register", "POST", {
        "username": recipient_username,
        "email": f"{recipient_username}@test.com",
        "password": "pass123"
    })

    # Get sender token
    login_resp = api_client("/login", "POST", {"username": sender_username, "password": "pass123"})
    token = login_resp.json()["access_token"]

    # Retrieve User objects from DB
    sender = db_session.query(User).filter_by(username=sender_username).first()
    recipient = db_session.query(User).filter_by(username=recipient_username).first()

    # Create 15 transactions directly in DB
    for i in range(15):
        tx = Transaction(
            sender_id=sender.id,
            receiver_id=recipient.id,
            amount=10,
            description=f"tx{i}"
        )
        db_session.add(tx)
    db_session.commit()

    # Verify transactions count
    count = db_session.query(Transaction).filter_by(sender_id=sender.id).count()
    print(f"\nTransactions in DB: {count}")

    # Test pagination
    resp = api_client("/transactions?page=1&per_page=5", token=token)
    assert resp.status_code == 200
    data = resp.json()
    print(f"First page transactions: {len(data['transactions'])} items")
    assert len(data["transactions"]) == 5
    assert data["pagination"]["total"] == 15
    assert data["pagination"]["pages"] == 3
    assert data["pagination"]["page"] == 1

    resp = api_client("/transactions?page=2&per_page=5", token=token)
    data = resp.json()
    assert len(data["transactions"]) == 5
    assert data["pagination"]["page"] == 2

def test_profile_update(api_client, db_session):
    username = generate_unique_username("profile")
    api_client("/register", "POST", {
        "username": username,
        "email": f"{username}@test.com",
        "password": "oldpass"
    })

    login_resp = api_client("/login", "POST", {"username": username, "password": "oldpass"})
    token = login_resp.json()["access_token"]

    # Update email
    new_email = f"{username}_new@test.com"
    resp = api_client("/profile", "PUT", {"email": new_email}, token=token)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Profile updated successfully"

    profile = api_client("/profile", token=token).json()
    assert profile["email"] == new_email

    # Update password
    new_pass = "newpass123"
    resp = api_client("/profile", "PUT", {"password": new_pass}, token=token)
    assert resp.status_code == 200

    login_resp = api_client("/login", "POST", {"username": username, "password": new_pass})
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

# Optional edge-case tests (you can add these as well)
def test_transfer_negative_amount(api_client, db_session):
    # similar pattern using unique users
    pass

def test_transfer_to_nonexistent_user(api_client, db_session):
    pass