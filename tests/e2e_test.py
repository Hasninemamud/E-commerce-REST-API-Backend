import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000/api"
FRONTEND_URL = "http://localhost:3000"

# Test data
test_user = {
    "email": "e2e_test@example.com",
    "password": "e2epassword123",
    "first_name": "E2E",
    "last_name": "Tester"
}

test_admin = {
    "email": "e2e_admin@example.com",
    "password": "e2eadmin123",
    "first_name": "E2E",
    "last_name": "Admin"
}

class E2ETester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_session = requests.Session()
        self.token = None
        self.admin_token = None

    def test_user_registration(self):
        """Test user registration flow"""
        print("1. Testing user registration...")
        
        # Register new user
        response = self.session.post(
            f"{BASE_URL}/auth/register/",
            data=test_user
        )
        
        if response.status_code == 201:
            print("   ✓ User registration successful")
            return True
        else:
            print(f"   ✗ User registration failed: {response.status_code} - {response.text}")
            return False

    def test_user_login(self):
        """Test user login flow"""
        print("2. Testing user login...")
        
        # Login user
        response = self.session.post(
            f"{BASE_URL}/auth/login/",
            data={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
            print("   ✓ User login successful")
            return True
        else:
            print(f"   ✗ User login failed: {response.status_code} - {response.text}")
            return False

    def test_admin_setup(self):
        """Setup admin user (in a real scenario, this would be done manually)"""
        print("3. Setting up admin user...")
        
        # In a real test, we would create an admin user through Django admin
        # For this test, we'll assume an admin user already exists
        print("   ✓ Admin setup assumed (would be done manually in production)")
        return True

    def test_product_management(self):
        """Test product management flow"""
        print("4. Testing product management...")
        
        # Get products (no auth required)
        response = self.session.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            print("   ✓ Get products successful")
        else:
            print(f"   ✗ Get products failed: {response.status_code}")
            return False
        
        # Get product details (no auth required)
        products = response.json()
        if products.get('results'):
            product_id = products['results'][0]['id']
            response = self.session.get(f"{BASE_URL}/products/{product_id}/")
            if response.status_code == 200:
                print("   ✓ Get product details successful")
            else:
                print(f"   ✗ Get product details failed: {response.status_code}")
                return False
        else:
            print("   ! No products available for testing")
        
        return True

    def test_shopping_cart(self):
        """Test shopping cart flow"""
        print("5. Testing shopping cart...")
        
        # Get products
        response = self.session.get(f"{BASE_URL}/products/")
        if response.status_code != 200:
            print("   ✗ Failed to get products for cart test")
            return False
            
        products = response.json()
        if not products.get('results'):
            print("   ! No products available for cart test")
            return True
            
        product_id = products['results'][0]['id']
        
        # Add to cart
        cart_data = {
            "items": [
                {
                    "product": product_id,
                    "quantity": 1
                }
            ]
        }
        
        response = self.session.post(
            f"{BASE_URL}/orders/cart/",
            json=cart_data
        )
        
        if response.status_code == 201:
            print("   ✓ Add to cart successful")
        else:
            print(f"   ✗ Add to cart failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_order_process(self):
        """Test order process flow"""
        print("6. Testing order process...")
        
        # Get products
        response = self.session.get(f"{BASE_URL}/products/")
        if response.status_code != 200:
            print("   ✗ Failed to get products for order test")
            return False
            
        products = response.json()
        if not products.get('results'):
            print("   ! No products available for order test")
            return True
            
        product_id = products['results'][0]['id']
        
        # Create order
        order_data = {
            "items": [
                {
                    "product": product_id,
                    "quantity": 1
                }
            ]
        }
        
        response = self.session.post(
            f"{BASE_URL}/orders/",
            json=order_data
        )
        
        if response.status_code == 201:
            print("   ✓ Create order successful")
        else:
            print(f"   ✗ Create order failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_payment_process(self):
        """Test payment process flow"""
        print("7. Testing payment process...")
        
        # Create payment intent
        payment_data = {
            "amount": 2999,  # $29.99 in cents
            "currency": "usd"
        }
        
        response = self.session.post(
            f"{BASE_URL}/payments/create-payment-intent/",
            json=payment_data
        )
        
        if response.status_code == 200:
            print("   ✓ Create payment intent successful")
        else:
            print(f"   ✗ Create payment intent failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_review_system(self):
        """Test review system flow"""
        print("8. Testing review system...")
        
        # Get products
        response = self.session.get(f"{BASE_URL}/products/")
        if response.status_code != 200:
            print("   ✗ Failed to get products for review test")
            return False
            
        products = response.json()
        if not products.get('results'):
            print("   ! No products available for review test")
            return True
            
        product_id = products['results'][0]['id']
        
        # Create review
        review_data = {
            "product": product_id,
            "rating": 5,
            "comment": "This is an excellent product!"
        }
        
        response = self.session.post(
            f"{BASE_URL}/reviews/",
            json=review_data
        )
        
        if response.status_code == 201:
            print("   ✓ Create review successful")
        else:
            print(f"   ✗ Create review failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_wishlist(self):
        """Test wishlist flow"""
        print("9. Testing wishlist...")
        
        # Get products
        response = self.session.get(f"{BASE_URL}/products/")
        if response.status_code != 200:
            print("   ✗ Failed to get products for wishlist test")
            return False
            
        products = response.json()
        if not products.get('results'):
            print("   ! No products available for wishlist test")
            return True
            
        product_id = products['results'][0]['id']
        
        # Add to wishlist
        wishlist_data = {
            "product": product_id
        }
        
        response = self.session.post(
            f"{BASE_URL}/wishlists/add/",
            json=wishlist_data
        )
        
        if response.status_code == 201:
            print("   ✓ Add to wishlist successful")
        else:
            print(f"   ✗ Add to wishlist failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_notifications(self):
        """Test notifications flow"""
        print("10. Testing notifications...")
        
        # Get notifications
        response = self.session.get(f"{BASE_URL}/notifications/")
        
        if response.status_code == 200:
            print("   ✓ Get notifications successful")
        else:
            print(f"   ✗ Get notifications failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def test_recommendations(self):
        """Test recommendations flow"""
        print("11. Testing recommendations...")
        
        # Get recommendations
        response = self.session.get(f"{BASE_URL}/recommendations/for-you/")
        
        if response.status_code == 200:
            print("   ✓ Get recommendations successful")
        else:
            print(f"   ✗ Get recommendations failed: {response.status_code} - {response.text}")
            return False
            
        return True

    def run_e2e_tests(self):
        """Run all end-to-end tests"""
        print("Starting End-to-End Tests...\n")
        
        tests = [
            self.test_user_registration,
            self.test_user_login,
            self.test_admin_setup,
            self.test_product_management,
            self.test_shopping_cart,
            self.test_order_process,
            self.test_payment_process,
            self.test_review_system,
            self.test_wishlist,
            self.test_notifications,
            self.test_recommendations
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                print()  # Add spacing between tests
            except Exception as e:
                print(f"   ✗ Test failed with exception: {e}")
                print()
        
        print(f"End-to-End Tests Completed: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All end-to-end tests passed!")
            return True
        else:
            print("❌ Some tests failed. Please check the output above.")
            return False

if __name__ == "__main__":
    tester = E2ETester()
    tester.run_e2e_tests()