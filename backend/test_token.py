import jwt
from datetime import datetime, timedelta, timezone

secret_key = "a13ce7904227e39f15528a97bd437bd04428266e39f8f31579b45bf957165327"
payload = {
    "username": "test_user",
    "role": "admin",
    "exp": datetime.now(timezone.utc) + timedelta(hours=1),
}

try:
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("JWT Token:", token)
except AttributeError as e:
    print("Error:", e)
