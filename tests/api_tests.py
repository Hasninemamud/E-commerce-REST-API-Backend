import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

# Test data
test_user = {
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

test_product = {
    "name": "Test Product",
    "description": "This is a test product",
    "price": 29.99,
    "category": 1
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def register_user(self):
        """Test user registration"""
        print("Testing user registration...")
        response = self.session.post(
            f"{BASE_URL}/auth/register/",
            data=test_user
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("Registration successful!")
            return True
        else:
            print(f"Registration failed: {response.text}")
            return False

    def login_user(self):
        """Test user login"""
        print("Testing user login...")
        response = self.session.post(
            f"{BASE_URL}/auth/login/",
            data={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
            print("Login successful!")
            return True
        else:
            print(f"Login failed: {response.text}")
            return False

    def get_user_profile(self):
        """Test getting user profile"""
        print("Testing get user profile...")
        response = self.session.get(f"{BASE_URL}/auth/user/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("User profile retrieved successfully!")
            return True
        else:
            print(f"Failed to get user profile: {response.text}")
            return False

    def get_products(self):
        """Test getting products"""
        print("Testing get products...")
        response = self.session.get(f"{BASE_URL}/products/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Products retrieved successfully!")
            return True
        else:
            print(f"Failed to get products: {response.text}")
            return False

    def run_tests(self):
        """Run all tests"""
        print("Starting API tests...\n")
        
        # Test registration
        if not self.register_user():
            print("Registration test failed. Stopping tests.")
            return
        
        print()
        
        # Test login
        if not self.login_user():
            print("Login test failed. Stopping tests.")
            return
        
        print()
        
        # Test get user profile
        if not self.get_user_profile():
            print("Get user profile test failed.")
        
        print()
        
        # Test get products
        if not self.get_products():
            print("Get products test failed.")
        
        print("\nAPI tests completed!")

if __name__ == "__main__":
    tester = APITester()
    tester.run_tests()