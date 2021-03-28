from django.urls import reverse
from rest_framework.test import APIClient
from django.conf import settings
from django.test import TestCase
#
#
# class MenusViewSetTest(TestCase):
#     """Testy dla widoków Menu."""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_users_statistic(self, _has_permission):
#         """Test statystyk."""
#         # url = reverse("users-statistic")
#         # with patch("users.authentication.requests.get") as request:
#         #     request.return_value = Mock(status_code=200, json=lambda: {})
#         #     response = self.client.get(url)
#         # statistic = response.json()
#         # self.assertEqual(response.status_code, 200)
#         # self.assertEqual(statistic["count"], 0)