"""Decode a JWT token to see what's inside"""
import requests
from jose import jwt

API_URL = "http://localhost:8000/api"
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"

# Login
print("Logging in...")
response = requests.post(
    f"{API_URL}/auth/login",
    json={"email": "admin@university.edu", "password": "admin123"}
)

if response.status_code == 200:
    data = response.json()
    token = data["access_token"]
    print(f"✓ Got token\n")
    
    # Decode token WITHOUT verification first to see payload
    print("Decoding token (no verification)...")
    try:
        payload_unverified = jwt.get_unverified_claims(token)
        print(f"Payload: {payload_unverified}")
        print(f"Sub value: {payload_unverified.get('sub')}")
        print(f"Sub type: {type(payload_unverified.get('sub'))}")
    except Exception as e:
        print(f"Error decoding: {e}")
    
    # Now try WITH verification
    print("\nDecoding token (with verification)...")
    try:
        payload_verified = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✓ Verification successful!")
        print(f"Payload: {payload_verified}")
    except Exception as e:
        print(f"✗ Verification failed: {e}")
else:
    print(f"Login failed: {response.text}")

