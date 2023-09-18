from rest_framework.test import APITestCase

from django.urls import reverse

class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            "username": "levin",
            "email": "levin@gmail.com",
            "password": "123"
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    