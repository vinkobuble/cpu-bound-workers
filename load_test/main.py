import os


from locust import HttpUser, task, between


class MultiplyMatrix(HttpUser):
    wait_time = between(1, 3)

    @task()
    def post_matrix_multiplication_job(self):
        self.client.post(
            "/matrix-multiplication/submit-job/",
            json={"a": {"data": [[1, 2, 3], [4, 5, 6]]}, "b": {"data": [[1, 2], [3, 4], [5, 6]]}}
        )
