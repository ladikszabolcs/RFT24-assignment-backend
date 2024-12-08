from api.models import User  # Az api.User importálása
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.test import TestCase

class APITestCase(TestCase):

    def setUp(self):
        # Létrehozzuk a teszt felhasználót
        self.user = User.objects.create_user(username='testuser', password='password')

        # Töröljük a felhasználóhoz tartozó összes meglévő tokent, ha van
        Token.objects.filter(user=self.user).delete()

        # Token generálása a felhasználóhoz
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()

    def test_api_token_auth(self):
        # POST kérést küldünk a /token/ endpointnak a felhasználó adatainkkal
        response = self.client.post(reverse('api_token_auth'), data={
            'username': 'testuser',
            'password': 'password'
        })
        # Ellenőrizzük, hogy a válasz státusza 200
        self.assertEqual(response.status_code, 200)

    def test_auth_me(self):
        # A token-t küldjük a kérés fejléceként
        response = self.client.get(
            reverse('auth_me'),
            HTTP_AUTHORIZATION='Token ' + self.token.key  # Helyes token formátum
        )
        # Ellenőrizzük, hogy a válasz státusza 200
        self.assertEqual(response.status_code, 200)
