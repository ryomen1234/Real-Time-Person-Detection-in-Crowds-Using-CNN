"""Test authentication flow"""
import requests

API_URL = "http://localhost:8000/api"

print("Testing Authentication Flow...\n")

# Step 1: Login
print("[1] Logging in as admin...")
response = requests.post(
    f"{API_URL}/auth/login",
    json={"email": "admin@university.edu", "password": "admin123"}
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data["access_token"]
    print(f"✓ Login successful!")
    print(f"Token (first 50 chars): {token[:50]}...")
    
    # Step 2: Try to get users with token
    print("\n[2] Trying to get users with token...")
    headers = {"Authorization": f"Bearer {token}"}
    response2 = requests.get(f"{API_URL}/users", headers=headers)
    print(f"Status: {response2.status_code}")
    
    if response2.status_code == 200:
        users = response2.json()
        print(f"✓ Got {len(users)} users!")
        for user in users[:3]:
            print(f"  - {user['name']} ({user['email']})")
    else:
        print(f"✗ Failed: {response2.text}")
else:
    print(f"✗ Login failed: {response.text}")

