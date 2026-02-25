# FinTech Banking System

A secure Flask-based digital banking application with JWT authentication, role-based access control, and a comprehensive test suite including API, UI, and database tests.

![Tests](https://github.com/your-username/your-repo-name/actions/workflows/test.yml/badge.svg)

## Features

- 🔐 User Registration & Login with JWT
- 👤 Profile Management (update email/password)
- 💰 Balance Inquiry
- 💸 Fund Transfer between users
- 📜 Transaction History with pagination
- 🛡️ Role-based access: regular users and admins
- 💵 Admin-only Deposit and Withdraw endpoints
- 🧪 Full test suite (pytest + Selenium + DB validation)
- 🤖 CI/CD with GitHub Actions

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Testing:** pytest, Selenium, requests, SQLAlchemy
- **CI/CD:** GitHub Actions

## Installation

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name