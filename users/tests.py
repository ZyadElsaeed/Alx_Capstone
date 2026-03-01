from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTests(APITestCase):
    """Tests for the user registration endpoint."""

    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "testuser")

    def test_register_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpass123",
            "password_confirm": "differentpass",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="strongpass123")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """Tests for the login endpoint."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpass123",
        )

    def test_login_success(self):
        data = {"username": "testuser", "password": "strongpass123"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
