from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthFlowTests(TestCase):
    def test_signup_login_logout(self):
        # Sign up
        response = self.client.post(reverse("signup"), {
            "username": "testuser",
            "password1": "testpass1234",
            "password2": "testpass1234"
        }, follow=True)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertContains(response, "Welcome, testuser")

        # Logout
        response = self.client.get(reverse("logout"), follow=True)
        self.assertNotIn("_auth_user_id", self.client.session)

        # Login
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass1234"
        }, follow=True)
        self.assertContains(response, "Welcome, testuser")
