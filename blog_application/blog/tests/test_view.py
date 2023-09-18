from .test_setup import TestSetup

from rest_framework import status

class TestView(TestSetup):

    def test_user_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_register(self):
        res = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    