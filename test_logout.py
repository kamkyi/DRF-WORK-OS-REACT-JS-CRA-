#!/usr/bin/env python3
"""
Test script for WorkOS logout flow
Run this from the backend directory to test the logout endpoint
"""

import requests
import json
import os


def test_logout_endpoint():
    """Test the /api/logout/ endpoint"""

    # Backend URL
    api_base = os.getenv("REACT_APP_API_BASE", "http://localhost:8000/api")
    logout_url = f"{api_base}/logout/"

    print(f"Testing logout endpoint: {logout_url}")

    try:
        # Test without WorkOS session cookie (should return fallback)
        response = requests.get(logout_url)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            if "logout_url" in data:
                print("✅ Logout endpoint working correctly!")
                print(f"   Logout URL: {data['logout_url']}")
                print(f"   Message: {data['message']}")
            else:
                print("❌ Response missing logout_url")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        print("   Make sure Django server is running on port 8000")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response: {e}")
        print(f"   Raw response: {response.text}")


if __name__ == "__main__":
    test_logout_endpoint()
