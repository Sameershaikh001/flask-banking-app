# Manual Testing Summary

This document outlines the manual testing performed on the FinTech Banking Application.

## 📁 Test Artifacts

- **Detailed Test Report (Google Sheets / Excel):**  
  [Link to Spreadsheet](https://docs.google.com/spreadsheets/d/1WJ0sYLkeUhKT2pQCQTeqe6HM7UEj5rphX6NZx1caqss/edit?usp=sharing)  
  

## ✅ Test Coverage

The manual test suite covers the following features:

- User Registration (positive, negative, edge cases)
- Login (valid, invalid credentials)
- Dashboard (admin vs regular user view)
- Fund Transfer (sufficient/insufficient balance, non-existent user)
- Profile Update (email, password)
- Transaction History (pagination, data correctness)
- Deposit & Withdraw (admin only)
- UI Responsiveness (mobile/desktop)

## 🧪 Testing Approach

- Each test case follows the format: **Feature, Test ID, Scenario, Steps, Data, Expected Result, Actual Result, Status, Date, Comments**.
- Tests were executed manually across different browsers (Chrome, Firefox) and device sizes.
- Defects found are logged in the spreadsheet with comments.

## 📅 Test Execution

- **Test Date Range:** (e.g., 2025-02-27 to 2025-02-28)
- **Tester:** (Your Name)
- **Environment:** Flask development server (local) / Render staging

## 🔗 Continuous Improvement

All failed tests are being tracked and will be addressed in upcoming sprints. This manual testing complements our automated CI pipeline (GitHub Actions) to ensure high software quality.