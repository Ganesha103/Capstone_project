import pickle

with open("cookies.pkl", "rb") as file:
    saved_cookies = pickle.load(file)
    print("Cookies in File:", saved_cookies)
