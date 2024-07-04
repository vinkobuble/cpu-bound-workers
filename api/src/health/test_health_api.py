from http import HTTPStatus
from unittest import TestCase
from fastapi.testclient import TestClient

from main import app


class TestHealthApi(TestCase):
    def setUp(self):
        self._client = TestClient(app)
        self._HEALTH_API_URL = app.url_path_for('health')

    def test_health_api(self):
        response = self._client.get(self._HEALTH_API_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_data = response.json()
        self.assertEqual(response_data["message"], "All system operating")
