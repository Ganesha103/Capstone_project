import time
from random import random

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_data import test_users
from cookie_handler import save_cookies, load_cookies
import random


@pytest.fixture(scope="function")
def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


@pytest.mark.parametrize("user", test_users)
def test_login(setup, user):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys(user["username"])
    driver.find_element(By.ID, "password").send_keys(user["password"])
    driver.find_element(By.ID, "login-button").click()

    save_cookies(driver)  # Save cookies after login

    if user["expected_result"] == "success":
        assert "inventory.html" in driver.current_url
    else:
        assert "Epic sadface" in driver.find_element(By.XPATH, "//h3[@data-test='error']").text


@pytest.mark.parametrize("user", test_users)
def test_login_via_cookies(setup, user):
    driver = setup
    driver.get("https://www.saucedemo.com/")

    load_cookies(driver)
    driver.refresh()

    assert "https://www.saucedemo.com/" in driver.current_url, "Cookie-based login failed!"

def test_login_guvi_user(setup):
    """Test whether guvi_user can log in successfully"""
    driver = setup

    # Enter login credentials
    driver.find_element(By.ID, "user-name").send_keys("guvi_user")
    driver.find_element(By.ID, "password").send_keys("Secret@123")
    driver.find_element(By.ID, "login-button").click()

    # Verify successful login
    assert "inventory.html" in driver.current_url, "Login failed for guvi_user!"


def test_logout(setup, user):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys(user["standard_user"])
    driver.find_element(By.ID, "password").send_keys(user["secret_sauce"])
    driver.find_element(By.ID, "login-button").click()

    time.sleep(10)

    # Click the burger menu
    menu_button = driver.find_element(By.XPATH, "//*[@id='react-burger-menu-btn']")
    menu_button.click()
    time.sleep(2)  # Allow the menu to fully expand

    # Click the logout button
    logout_button = driver.find_element(By.XPATH, "//*[@id='logout_sidebar_link']")
    logout_button.click()

    # Verify logout success
    assert "https://www.saucedemo.com/" in driver.current_url, "Logout failed!"


def test_logout_button_visibility(setup, user):
    driver = setup
    driver.find_element(By.ID, "user-name").send_keys(user["standard_user"])
    driver.find_element(By.ID, "password").send_keys(user["secret_sauce"])
    driver.find_element(By.ID, "login-button").click()

    menu_button = driver.find_element(By.XPATH, "//*[@id='react-burger-menu-btn']")
    menu_button.click()
    time.sleep(4)

    assert driver.find_element(By.ID, "logout_sidebar_link").is_displayed(), "Logout button not visible!"

def test_cart_button_visibility(setup):
    """Verify if the cart button is visible after login"""
    driver = setup

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Check if the cart button is visible
    cart_button = driver.find_element(By.XPATH, "//*[@id='shopping_cart_container']/a")
    assert cart_button.is_displayed(), "Cart button is not visible!"


def test_random_product_selection(setup):
    """Select four random products from inventory and fetch their names & prices"""
    driver = setup

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Locate product elements
    product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    product_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    # Ensure we have at least six products
    assert len(product_names) == 6, "Inventory does not have six products!"

    time.sleep(9)

    # Select four random products
    selected_indices = random.sample(list(range(6)), 4)
    selected_products = [(product_names[i].text, product_prices[i].text) for i in selected_indices]
    time.sleep(9)

    print("\nSelected Products:")
    for name, price in selected_products:
        print(f"Product: {name}, Price: {price}")

    assert len(selected_products) == 4, "Failed to select four random products!"

def test_verify_cart_contents(setup):
    """Add products to cart, verify cart button, and fetch product details from the cart"""
    driver = setup

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    time.sleep(9)

    # Locate product buttons and add two items to cart
    add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    assert len(add_buttons) >= 2, "Not enough products available to add to cart!"

    add_buttons[0].click()
    add_buttons[1].click()

    # Click the cart button
    cart_button = driver.find_element(By.ID, "shopping_cart_container")
    cart_button.click()

    # Fetch product details from the cart
    cart_products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    cart_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    assert len(cart_products) > 0, "Cart is empty!"

    print("\nProducts in Cart:")
    for name, price in zip(cart_products, cart_prices):
        print(f"Product: {name.text}, Price: {price.text}")

    assert len(cart_products) == 2, "Mismatch in expected cart items!"

def test_checkout_process(setup):
    """Test checkout process including user details, screenshot, and final confirmation"""
    driver = setup

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    time.sleep(9)

    # Locate product buttons and add two items to the cart
    add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    assert len(add_buttons) >= 2, "Not enough products available to add to cart!"

    add_buttons[0].click()
    add_buttons[1].click()

    # Click the cart button
    cart_button = driver.find_element(By.ID, "shopping_cart_container")
    cart_button.click()

    # Verify product details before checkout
    cart_products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    cart_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    assert len(cart_products) > 0, "Cart is empty!"

    print("\nProducts in Cart Before Checkout:")
    for name, price in zip(cart_products, cart_prices):
        print(f"Product: {name.text}, Price: {price.text}")

    # Click checkout button
    driver.find_element(By.ID, "checkout").click()

    # Enter user details
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # Take screenshot of checkout overview
    time.sleep(2)
    driver.save_screenshot("checkout_overview.png")
    print("✅ Screenshot of checkout overview saved!")

    # Verify product details in checkout overview
    overview_products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    overview_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    assert len(overview_products) == len(cart_products), "Mismatch in products between cart and checkout!"

    print("\nProducts in Checkout Overview:")
    for name, price in zip(overview_products, overview_prices):
        print(f"Product: {name.text}, Price: {price.text}")

    # Click finish button and verify confirmation message
    driver.find_element(By.ID, "finish").click()
    confirmation_msg = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))).text

    assert "Thank you for your order!" in confirmation_msg, "Checkout confirmation failed!"
    print("✅ Checkout completed successfully!")