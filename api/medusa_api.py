from playwright.async_api import APIResponse
from playwright.sync_api import (
    APIRequestContext,
)  # APIRequestContext это замена библиотеке requests
from faker import Faker

fake = Faker()


class MedusaAPIClient:
    # Класс для работы с бэкендом Medusa (API),
    def __init__(self, request_context: APIRequestContext):
        self.api = request_context
        self.token = None

    @property  # декоратор property позволяет использовать функцию как переменную то есть можно будет написать self.auth_headers
    def auth_headers(self) -> dict:
        if not self.token:
            raise Exception("Сначала нужно вызвать метод login()!")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def login(self, email: str, password: str) -> APIResponse:

        response = self.api.post(
            "/auth/user/emailpass", data={"email": email, "password": password}
        )
        if response.status == 200:
            body = response.json()
            self.token = body.get("token") or body.get("access_token")
        return response

    def generate_publishable_key(
        self,
    ) -> (
        str
    ):  # этот метод создает публичный ключ для работы с витриной (мне он нужен чтобы создать корзину)
        print(f"\n[API] Генерируем ключ для корзины")
        response = self.api.post(
            "/admin/api-keys",
            data={"title": "Test Storefront Key", "type": "publishable"},
            headers=self.auth_headers,
        )
        assert response.status == 200, f"Ошибка создания ключа: {response.text()}"

        pk_key = response.json()["api_key"]["token"]
        print(f"[API] Ключ получен: {pk_key}")
        return pk_key

    def get_default_sales_channel_id(self) -> str:
        response = self.api.get("/admin/sales-channels", headers=self.auth_headers)
        assert response.status == 200, f"Ошибка получения канала: {response.text()}"
        return response.json()["sales_channels"][0]["id"]

    def create_product(self, payload: dict):

        response = self.api.post(
            "/admin/products", data=payload, headers=self.auth_headers
        )
        # product_id = response.json()["product"]["id"]
        # print(f"[API] Товар успешно создан, его id: {product_id}")
        return response

    def get_product(self, product_id: str) -> APIResponse:

        response = self.api.get(
            f"/admin/products/{product_id}", headers=self.auth_headers
        )
        return response

    def delete_product(self, product_id: str) -> APIResponse:
        print(f"[API] Удаляем товар: {product_id}")
        response = self.api.delete(
            f"/admin/products/{product_id}", headers=self.auth_headers
        )
        print(f"[API] Товар {product_id} удален!")
        return response

    def create_empty_cart(
        self, pk_key: str, sales_channel_id: str, region_id: str
    ) -> APIResponse:
        response = self.api.post(
            "/store/carts",
            data={"sales_channel_id": sales_channel_id, "region_id": region_id},
            headers={
                "Content-Type": "application/json",
                "x-publishable-api-key": pk_key,
            },
        )
        return response

    def add_item_to_cart(
        self, cart_id: str, variant_id: str, pk_key: str, quantity: int = 1
    ) -> APIResponse:
        payload = {
            "variant_id": variant_id,
            "quantity": quantity,
        }
        response = self.api.post(
            f"/store/carts/{cart_id}/line-items",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-publishable-api-key": pk_key,
            },
        )
        return response

    def get_default_region_info(self) -> tuple:
        response = self.api.get("/admin/regions", headers=self.auth_headers)
        assert response.status == 200, f"Ошибка в получении региона: {response.text()}"
        region = response.json()["regions"][0]
        return region["id"], region["currency_code"]

    def get_orders(self) -> APIResponse:
        response = self.api.get("/admin/orders", headers=self.auth_headers)
        return response

    def get_order_by_id(self, order_id: str) -> APIResponse:
        response = self.api.get(f"/admin/orders/{order_id}", headers=self.auth_headers)
        return response
