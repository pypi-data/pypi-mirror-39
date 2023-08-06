from django.test import TestCase
from django.urls import reverse

class HealthCheckApiTestCase(TestCase):

    def setUp(self):
        self.url = reverse('health-list')
        self.result = self.client.get(self.url)

    def test_is_ok(self):
        self.assertEqual(self.result.status_code, 200)
