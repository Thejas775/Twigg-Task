#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test the FastAPI endpoints."""

    print("🧪 Testing Investment Holdings API\n")

    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   Completed  Root endpoint working\n")
    except Exception as e:
        print(f"   Failed: Root endpoint failed: {e}\n")
        return

    # Test 2: Register a new user
    print("2. Testing user registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   User created: {response.json()['email']}")
            print("   Completed  Registration working\n")
        else:
            print(f"   Response: {response.json()}")
            print("     Registration may have failed (user might already exist)\n")
    except Exception as e:
        print(f"   Failed: Registration failed: {e}\n")

    # Test 3: Login with existing user
    print("3. Testing user login...")
    login_data = {
        "email": "thejas@gmail.com",
        "password": "pass"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   Token received: {access_token[:20]}...")
            print("   Completed  Login working\n")

            # Test 4: Get holdings with authentication
            print("4. Testing holdings endpoint...")
            headers = {"Authorization": f"Bearer {access_token}"}

            try:
                holdings_response = requests.get(f"{BASE_URL}/holdings/", headers=headers)
                print(f"   Status: {holdings_response.status_code}")
                if holdings_response.status_code == 200:
                    holdings_data = holdings_response.json()
                    print(f"   Holdings count: {len(holdings_data['holdings'])}")
                    print(f"   Total current value: ${holdings_data['insights']['total_current_value']}")
                    print(f"   Total gain/loss: ${holdings_data['insights']['total_gain_loss']}")
                    print("   Completed  Holdings endpoint working\n")

                    print("📊 Sample Holdings Data:")
                    for holding in holdings_data['holdings']:
                        print(f"   - {holding['asset_symbol']}: {holding['quantity']} shares")
                        print(f"     Current value: ${holding['current_value']}")
                        print(f"     Gain/Loss: ${holding['gain_loss']} ({float(holding['gain_loss_percentage']):.2f}%)")
                else:
                    print(f"   Response: {holdings_response.json()}")
                    print("   Failed: Holdings endpoint failed\n")
            except Exception as e:
                print(f"   Failed: Holdings request failed: {e}\n")

        else:
            print(f"   Response: {response.json()}")
            print("   Failed: Login failed\n")
    except Exception as e:
        print(f"   Failed: Login failed: {e}\n")

    # Test 5: Test unauthorized access
    print("5. Testing unauthorized access...")
    try:
        response = requests.get(f"{BASE_URL}/holdings/")
        print(f"   Status: {response.status_code}")
        if response.status_code in [401, 403]:
            print("   Completed  Unauthorized access properly blocked\n")
        else:
            print("     Expected 401/403 status for unauthorized access\n")
    except Exception as e:
        print(f"   Failed: Unauthorized test failed: {e}\n")

    print("API testing complete!")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running: uvicorn app.main:app --reload")
    print("Press Enter to continue with testing...")
    input()
    test_api_endpoints()