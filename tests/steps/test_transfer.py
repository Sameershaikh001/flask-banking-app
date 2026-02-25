from behave import given, when, then
import requests
from app.models import User, Transaction
from app import db

BASE_URL = "http://127.0.0.1:5000"

@given("the following users exist")
def step_impl(context):
    for row in context.table:
        # Create user via API or directly in DB
        user = User(username=row["username"], email=row["email"], balance=float(row["balance"]))
        user.set_password(row["password"])
        db.session.add(user)
    db.session.commit()

@when("Alice logs in")
def step_impl(context):
    resp = requests.post(f"{BASE_URL}/login", json={"username": "alice", "password": "pass"})
    assert resp.status_code == 200
    context.token = resp.json()["access_token"]

@when("she transfers {amount:d} to Bob")
def step_impl(context, amount):
    headers = {"Authorization": f"Bearer {context.token}"}
    resp = requests.post(f"{BASE_URL}/transfer", json={"to_username": "bob", "amount": amount}, headers=headers)
    assert resp.status_code == 200
    context.transfer_response = resp.json()

@then("Alice's balance should be {expected:d}")
def step_impl(context, expected):
    user = User.query.filter_by(username="alice").first()
    assert user.balance == expected

@then("Bob's balance should be {expected:d}")
def step_impl(context, expected):
    user = User.query.filter_by(username="bob").first()
    assert user.balance == expected

@then("a transaction record should exist between them")
def step_impl(context):
    alice = User.query.filter_by(username="alice").first()
    bob = User.query.filter_by(username="bob").first()
    tx = Transaction.query.filter_by(sender_id=alice.id, receiver_id=bob.id).first()
    assert tx is not None
    assert tx.amount == 100