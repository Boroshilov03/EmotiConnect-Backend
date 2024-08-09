from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
    
    def test_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone_number': '1234567890'
        }, format='multipart')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('username', response.json())
    
    def test_signin(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        
        response = self.client.post(self.signin_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())
