import time
from locust import HttpUser, task, between


class FlaskAPITestUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    @task(3)  # Weight: 30% of requests
    def health_check(self):
        with self.client.get("/api/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed with status {response.status_code}")

    @task(2)  # Weight: 20% of requests
    def get_hello(self):
        with self.client.get("/api/hello?name=LoadTest", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Hello endpoint failed with status {response.status_code}")

    @task(4)  # Weight: 40% of requests
    def get_items(self):
        with self.client.get("/api/items", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get items failed with status {response.status_code}")

    @task(1)  # Weight: 10% of requests
    def get_item_by_id(self):
        # Test different item IDs
        import random
        item_ids = [1, 2, 3, 999]  # Include non-existent ID
        item_id = random.choice(item_ids)
        with self.client.get(f"/api/items/{item_id}", catch_response=True) as response:
            if item_id <= 3 and response.status_code == 200:
                response.success()
            elif item_id == 999 and response.status_code == 404:
                response.success()  # Expected for non-existent item
            else:
                response.failure(f"Get item {item_id} failed with status {response.status_code}")

    @task(1)  # Weight: 10% of requests
    def create_item(self):
        # Simulate creating items with different data
        import random
        item_data = {
            "name": f"Load Test Item {random.randint(1, 1000)}",
            "description": f"Description for load test item {random.randint(1, 1000)}"
        }
        with self.client.post("/api/items", json=item_data, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Create item failed with status {response.status_code}")


# Custom event listeners for detailed reporting
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Load test starting...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test stopping...")

@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    print(f"Spawning complete. Total users: {user_count}")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    if exception:
        print(f"Request failed: {name} - {exception}")
    elif response and response.status_code >= 400:
        print(f"Request error: {name} - Status: {response.status_code}")