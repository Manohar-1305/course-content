import pytest
from app import app

@pytest.fixture
def client():
    # Set up a test client for the app
    app.testing = True
    with app.test_client() as client:
        yield client

# Test the login page (GET request)
def test_login_page_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data  # Check if 'Login' appears in the response
    
    # Test login functionality with valid credentials (POST request)
def test_login_valid(self):
    with self.app:
        # Perform login and check redirect
        response = self.app.post('/login', data={'username': 'admin', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect to welcome page

        # Follow the redirect
        response = self.app.get(response.headers['Location'])
        self.assertEqual(response.status_code, 200)  # Should load the welcome page
        self.assertIn(b'Welcome', response.data)  # Check if 'Welcome' appears in the response

    
    # Test login functionality with invalid credentials (POST request)
def test_login_valid(self):
    with self.app:
        response = self.app.post('/login', data={'username': 'admin', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Should redirect to welcome page
        self.assertEqual(response.headers['Location'], '/welcome')  # Check the redirect location

    
    # Test the register page (GET request)
    def test_register_page_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)  # Check if 'Register' appears in the response
    
    # Test register functionality with new username (POST request)
    def test_register_new_user(self):
        response = self.app.post('/register', data={'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertIn(b'Registration successful!', response.data)
    
    # Test register functionality with existing username (POST request)
    def test_register_existing_user(self):
        response = self.app.post('/register', data={'username': 'admin', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists. Choose a different username.', response.data)
    
    # Test the welcome page (GET request)
    def test_welcome_page_get(self):
        with self.app:
            self.app.post('/login', data={'username': 'admin', 'password': 'password123'})
            response = self.app.get('/welcome')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome', response.data)
    
    # Test the logout functionality
    def test_logout(self):
        with self.app:
            self.app.post('/login', data={'username': 'admin', 'password': 'password123'})
            response = self.app.get('/logout')
            self.assertEqual(response.status_code, 302)  # Should redirect to login
            self.assertIn(b'You have been logged out.', response.data)

    # Test the course page (GET request)
    def test_course_page_get(self):
        with self.app:
            self.app.post('/login', data={'username': 'admin', 'password': 'password123'})
            self.app.post('/welcome', data={'subscribe': 'true'})
            response = self.app.get('/course')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Course', response.data)
    
    # Test health check endpoint
    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OK', response.data)

if __name__ == '__main__':
    unittest.main()
