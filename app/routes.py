from locust import HttpUser, task, between
from locust.exception import StopUser


class RevoShopUser(HttpUser):
    wait_time = between(1, 2)

    product_id = 66
    user_id = 2

    def stop_user(self):
        raise StopUser()

    @task
    def user_journey(self):
        response = self.client.get(
            "/products",
            name="GET /products",
        )

        if response.status_code != 200:
            print(
                f"[ERROR] GET /products -> "
                f"status={response.status_code}, "
                f"error={response.error}"
            )
            self.stop_user()

        try:
            products = response.json()
        except Exception as exc:
            print(f"[ERROR] Invalid JSON /products: {exc}")
            self.stop_user()

        if not products:
            print("[ERROR] /products returned empty list")
            self.stop_user()

        response = self.client.get(
            f"/products/{self.product_id}",
            name="GET /products/<id>",
        )

        if response.status_code != 200:
            print(
                f"[ERROR] GET /products/{self.product_id} -> "
                f"status={response.status_code}, "
                f"error={response.error}"
            )
            self.stop_user()

        order_data = {
            "user_id": self.user_id,
            "items": [
                {
                    "product_id": self.product_id,
                    "quantity": 1,
                }
            ],
        }

        response = self.client.post(
            "/orders",
            json=order_data,
            name="POST /orders",
        )

        if response.status_code not in (200, 201):
            print(
                f"[ERROR] POST /orders -> "
                f"status={response.status_code}, "
                f"error={response.error}, "
                f"response={response.text[:300]}"
            )
            self.stop_user()

        try:
            order = response.json()
        except Exception as exc:
            print(f"[ERROR] Invalid JSON /orders: {exc}")
            self.stop_user()

        order_id = order.get("id")

        if not order_id:
            print(f"[ERROR] Order ID tidak ditemukan: {order}")
            self.stop_user()

        response = self.client.get(
            f"/orders/{order_id}",
            name="GET /orders/<id>",
        )

        if response.status_code != 200:
            print(
                f"[ERROR] GET /orders/{order_id} -> "
                f"status={response.status_code}, "
                f"error={response.error}, "
                f"response={response.text[:300]}"
            )
            self.stop_user()

        self.stop_user()
