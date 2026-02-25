import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLoginUI:
    def test_login_page_loads(self, driver, base_url):
        driver.get(base_url + "/login-page")
        assert "Login" in driver.title
        assert driver.find_element(By.ID, "username").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()

    def test_login_success(self, driver, base_url, api_client):
        # Create a test user via API
        api_client("/register", "POST", {"username": "uitest", "email": "ui@test.com", "password": "pass"})
        driver.get(base_url + "/login-page")
        driver.find_element(By.ID, "username").send_keys("uitest")
        driver.find_element(By.ID, "password").send_keys("pass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Wait for redirect to dashboard
        WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url
        # Check balance element exists
        balance_elem = driver.find_element(By.ID, "balance")
        assert balance_elem.text != "Loading..."

    def test_login_failure(self, driver, base_url):
        driver.get(base_url + "/login-page")
        driver.find_element(By.ID, "username").send_keys("wrong")
        driver.find_element(By.ID, "password").send_keys("wrong")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Wait for error message
        msg = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "message")))
        assert "Invalid credentials" in msg.text

class TestDashboardUI:
    def test_dashboard_loads_after_login(self, driver, base_url, api_client):
        # Create and login user via UI
        api_client("/register", "POST", {"username": "dashuser", "email": "dash@test.com", "password": "pass"})
        driver.get(base_url + "/login-page")
        driver.find_element(By.ID, "username").send_keys("dashuser")
        driver.find_element(By.ID, "password").send_keys("pass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))
        # Check balance displayed
        balance = driver.find_element(By.ID, "balance").text
        assert "₹" in balance

class TestTransferUI:
    def test_transfer_page_loads(self, driver, base_url, api_client):
        # Create a dedicated user via API
        username = "uitest_transfer"
        password = "pass123"
        api_client("/register", "POST", {
            "username": username,
            "email": f"{username}@test.com",
            "password": password
        })
        login_resp = api_client("/login", "POST", {"username": username, "password": password})
        token = login_resp.json().get("access_token")
        assert token is not None, "Failed to obtain token"

        # Set token in localStorage and navigate
        driver.get(base_url + "/login-page")
        driver.execute_script(f"localStorage.setItem('access_token', '{token}');")
        driver.get(base_url + "/dashboard")

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "balance"))
        )
        transfer_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Money"))
        )
        transfer_link.click()
        WebDriverWait(driver, 5).until(EC.url_contains("/transfer-page"))
        assert "Transfer" in driver.title