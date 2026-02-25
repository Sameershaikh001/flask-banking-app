from . import db
from .models import Transaction

def transfer_funds(sender, receiver, amount, description=''):
    """
    Perform fund transfer between two users.
    Returns Transaction object if successful, else None.
    """
    try:
        sender.balance -= amount
        receiver.balance += amount

        transaction = Transaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=amount,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        print(f"Transfer failed: {e}")
        return None

def deposit_funds(user, amount):
    """
    Add funds to user's balance.
    Returns updated balance.
    """
    user.balance += amount
    db.session.commit()
    return user.balance

def withdraw_funds(user, amount):
    """
    Withdraw funds from user's balance if sufficient.
    Returns updated balance.
    """
    if user.balance < amount:
        raise ValueError("Insufficient balance")
    user.balance -= amount
    db.session.commit()
    return user.balance