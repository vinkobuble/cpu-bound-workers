import json
from http import HTTPStatus
from unittest import TestCase
from fastapi.testclient import TestClient

from main import app
from .schema import MultiplyMatrices, Matrix


class TestMatrixMultiplication(TestCase):
    def setUp(self):
        self._client = TestClient(app)
        self._MATRIX_MULTIPLICATION_SUBMIT_JOB_API_URL = app.url_path_for('matrix_multiplication_submit_job')

    def test_matrix_multiplication_submit_job(self):
        response = self._client.post(
            self._MATRIX_MULTIPLICATION_SUBMIT_JOB_API_URL,
            json=json.loads(MultiplyMatrices(
                a=Matrix(
                    data=[
                        [1, 2, 3],
                        [4, 5, 6],
                    ],
                ),
                b=Matrix(
                    data=[
                        [1, 2],
                        [3, 4],
                        [5, 6],
                    ],
                ),
            ).model_dump_json())
        )
        self.assertEqual(HTTPStatus.OK, response.status_code, response.content)

        response_data = response.json()
        self.assertEqual("scheduled", response_data["message"])
