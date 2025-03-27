# todolist/tests.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class AuthTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        # Test user data
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

        # Create a user for login tests
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Verify password is hashed
        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('testpassword123'))

        # Verify response doesn't contain raw password
        self.assertNotIn('password', response.data)

    def test_register_user_missing_fields(self):
        """Test registration with missing required fields"""
        invalid_data = {
            'username': 'partialuser',
            'password': 'partialpass123'
            # email is missing
        }

        response = self.client.post(
            self.register_url,
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_success(self):
        """Test successful login returns token"""
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123'
        }

        response = self.client.post(
            self.login_url,
            login_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)

    def test_login_wrong_password(self):
        """Test login with wrong password"""
        login_data = {
            'username': 'existinguser',
            'password': 'wrongpassword'
        }

        response = self.client.post(
            self.login_url,
            login_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        login_data = {
            'username': 'nonexistent',
            'password': 'doesntmatter'
        }

        response = self.client.post(
            self.login_url,
            login_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)