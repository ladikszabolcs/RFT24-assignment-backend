from django.test import TestCase
from django.test import TestCase
import requests

BASE_URL = "http://127.0.0.1:8000/"  # Lokális backend URL

class APITestCase(TestCase):
    def test_health_check(self):
        """Teszteljük, hogy az API fut-e."""
        response = requests.get(f"{BASE_URL}health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "ok")

    def test_get_all_courses(self):
        """Teszteljük az összes kurzus lekérdezését."""
        response = requests.get(f"{BASE_URL}api/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_login(self):
        """Teszteljük a bejelentkezési funkciót."""
        payload = {
            "username": "student",
            "password": "StudentDraken123"
        }
        response = requests.post(f"{BASE_URL}auth/login/", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_create_course(self):
        """Teszteljük új kurzus létrehozását (admin felhasználóval)."""
        token = self._get_auth_token("administrator", "DrakenAdmin456")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "name": "New Test Course",
            "description": "This is a test course"
        }
        response = requests.post(f"{BASE_URL}api/courses/", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    def _get_auth_token(self, username, password):
        """Segédfüggvény az autentikációs token lekéréséhez."""
        payload = {"username": username, "password": password}
        response = requests.post(f"{BASE_URL}auth/login/", json=payload)
        return response.json().get("token")


