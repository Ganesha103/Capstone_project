import pickle
import os

def save_cookies(driver, file_path="cookies.pkl"):
    cookies = driver.get_cookies()
    print("Saved Cookies:", cookies)  # Debugging Step
    if cookies:
        with open(file_path, "wb") as file:
            pickle.dump(cookies, file)
    else:
        print("No cookies found. Login might have failed.")

def load_cookies(driver, file_path="cookies.pkl"):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            cookies = pickle.load(file)
            print("Loading Cookies:", cookies)  # Debugging Step
            for cookie in cookies:
                if "domain" in cookie:
                    cookie["domain"] = ".saucedemo.com"
                driver.add_cookie(cookie)
