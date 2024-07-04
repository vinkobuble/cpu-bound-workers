import os
from http import HTTPStatus
from unittest import TestCase
from unittest import mock

from fastapi.testclient import TestClient

from main import app
from .schema import MultiplyMatricesRequestBody, Matrix


class TestMatrixMultiplication(TestCase):
    def setUp(self):
        self._client = TestClient(app)
        self._MATRIX_MULTIPLICATION_SUBMIT_JOB_API_URL = app.url_path_for('matrix_multiplication_submit_job')

    @mock.patch("rmq_setup.pika_setup.channel.basic_publish", return_value=None)
    def test_matrix_multiplication_submit_job(self, basic_publish_mock: mock.Mock):
        body = MultiplyMatricesRequestBody(
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
            )
        response = self._client.post(
            self._MATRIX_MULTIPLICATION_SUBMIT_JOB_API_URL,
            json=body.model_dump()
        )
        self.assertEqual(HTTPStatus.OK, response.status_code, response.content)

        response_data = response.json()
        self.assertEqual("scheduled", response_data["message"])

        basic_publish_mock.assert_called_once_with(
            exchange=os.environ['MATRIX_MULTIPLICATION_EXCHANGE'],
            routing_key=os.environ['MATRIX_MULTIPLICATION_WORKER_ROUTING_KEY'],
            body=body.model_dump_json().encode()
        )

    def test_invalid_matrix_raises_error(self):
        with self.assertRaises(ValueError):
            MultiplyMatricesRequestBody(
                a=Matrix(
                    data=[
                        [1, 2],
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
            )
