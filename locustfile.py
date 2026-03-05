from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hit_endpoint(self):
        self.client.get("/")

    @task
    def hit_route(self):
        num_stops = random.randint(2,10)
        coordinates = [
            {
                "lat": random.uniform(41.60, 42.05),
                "lon": random.uniform(-87.95, -87.50)
            }
            for _ in range(num_stops)
        ]
        
        self.client.post(
            "/route",
            json={"coordinates": coordinates}
        )