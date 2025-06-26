from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

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

class FileUploadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fileuser", password="testpass1234")
        self.client.login(username="fileuser", password="testpass1234")

    def test_upload_csv(self):
        csv_content = b"symbol,date,open,high,low,close,volume\nAAPL,2021-01,100,110,90,105,1000000\n"
        response = self.client.post(
            reverse("upload_csv"),
            {"csv_file": SimpleUploadedFile("data.csv", csv_content)},
            follow=True,
        )
        self.assertContains(response, "CSV uploaded successfully.")
        # Download uploaded CSV
        response = self.client.get(reverse("download_uploaded_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AAPL,2021-01,100,110,90,105,1000000", response.content)

    def test_upload_instructions(self):
        md_content = b"# Instructions\nDo something smart."
        response = self.client.post(
            reverse("upload_instructions"),
            {"instructions_file": SimpleUploadedFile("instructions.md", md_content)},
            follow=True,
        )
        self.assertContains(response, "Instructions uploaded successfully.")
        # Download uploaded instructions
        response = self.client.get(reverse("download_uploaded_instructions"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Do something smart.", response.content)

class InstructionsDisplayTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mduser", password="testpass1234")
        self.client.login(username="mduser", password="testpass1234")

    def test_view_default_instructions(self):
        self.client.logout()
        response = self.client.get(reverse("view_instructions"))
        self.assertContains(response, "Default Instructions")
        self.assertContains(response, "# Sample Instructions")

    def test_view_uploaded_instructions(self):
        # Upload instructions.md
        md_content = b"# My Custom Instructions\nDo something unique."
        self.client.post(
            reverse("upload_instructions"),
            {"instructions_file": SimpleUploadedFile("instructions.md", md_content)},
            follow=True,
        )
        response = self.client.get(reverse("view_instructions"))
        self.assertContains(response, "Your Uploaded Instructions")
        self.assertContains(response, "Do something unique.")
