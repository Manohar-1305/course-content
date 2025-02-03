import pytest
from app import app

@pytest.fixture
def client():
    """Fixture to set up a test client for the app."""
    app.testing = True
    with app.test_client() as client:
        yield client  # This will provide the client to the test functions

def test_login_page_get(client):
    """Test the login page (GET request)."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data  

def test_login_invalid(client):
    """Test login functionality with invalid credentials (POST request)."""
    response = client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'})
    assert response.status_code == 200  # Should stay on the login page
    assert b'Invalid password. Please try again.' in response.data  # Check for the correct error message

    # Alternatively, if you want to check for "User not found":
    response = client.post('/login', data={'username': 'nonexistent', 'password': 'wrongpassword'})
    assert response.status_code == 200  # Should stay on the login page
    assert b'User not found. Please register.' in response.data  # Check for the correct error message





    # Follow the redirect
    response = client.get(response.headers['Location'])
    assert response.status_code == 200  # Should load the welcome page
    assert b'Welcome' in response.data  # Check if 'Welcome' appears in the response

def test_login_invalid(client):
    """Test login functionality with invalid credentials (POST request)."""
    response = client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'})
    assert response.status_code == 200  # Should stay on the login page
    assert b'Invalid credentials' in response.data  # Check error message

def test_register_page_get(client):
    """Test the register page (GET request)."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data  # Check if 'Register' appears in the response

def test_register_new_user(client):
    """Test register functionality with new username (POST request)."""
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 302  # Should redirect to login page
    assert b'Registration successful!' in response.data

def test_register_existing_user(client):
    """Test register functionality with existing username (POST request)."""
    response = client.post('/register', data={'username': 'admin', 'password': 'password123'})
    assert response.status_code == 200
    assert b'Username already exists. Choose a different username.' in response.data

def test_welcome_page_get(client):
    """Test the welcome page (GET request)."""
    # Simulate login and check the welcome page
    client.post('/login', data={'username': 'admin', 'password': 'password123'})
    response = client.get('/welcome')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_logout(client):
    """Test the logout functionality."""
    # Simulate login and logout
    client.post('/login', data={'username': 'admin', 'password': 'password123'})
    response = client.get('/logout')
    assert response.status_code == 302  # Should redirect to login
    assert b'You have been logged out.' in response.data

def test_course_page_get(client):
    """Test the course page (GET request)."""
    # Simulate login and course subscription
    client.post('/login', data={'username': 'admin', 'password': 'password123'})
    client.post('/welcome', data={'subscribe': 'true'})
    response = client.get('/course')
    assert response.status_code == 200
    assert b'Course' in response.data

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'OK' in response.data

if __name__ == '__main__':
    unittest.main()
