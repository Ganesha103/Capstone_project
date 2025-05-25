test_users = [
    {"username": "standard_user", "password": "secret_sauce", "expected_result": "success"},
    {"username": "problem_user", "password": "secret_sauce", "expected_result": "success"},
    {"username": "performance_glitch_user", "password": "secret_sauce", "expected_result": "success"},
    {"username": "locked_out_user", "password": "secret_sauce", "expected_result": "failure"},
    {"username": "guvi_user", "password": "Secret@123", "expected_result": "success"}
]
