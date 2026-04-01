import allure
import pytest


@allure.epic("Корзина и заказы")
@allure.feature("API Корзины")
@allure.title("Успешный создание корзины и добавление товара")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.smoke
def test_add_item_to_cart_success(api_client, generate_product_payload, empty_cart_id):
    cart_id, pk_key, sc_id, currency = empty_cart_id
    with allure.step("Создаем тестовый товар"):
        payload = generate_product_payload(price_usd=250)
        payload["sales_channels"] = [{"id": sc_id}]
        payload["variants"][0]["prices"][0]["currency_code"] = currency
        prod_res = api_client.create_product(payload)
        assert prod_res.status == 200
        product_id = prod_res.json()["product"]["id"]
        variant_id = prod_res.json()["product"]["variants"][0]["id"]

    with allure.step(f"Добавляем вариант товара в корзину: {cart_id}"):
        add_res = api_client.add_item_to_cart(cart_id, variant_id, pk_key=pk_key)
        assert add_res.status == 200, f"Товар не добавился: {add_res.text()}"
        assert len(add_res.json()) == 1, "Корзина пустая"

    with allure.step("Удаляем тестовый товар"):
        api_client.delete_product(product_id)


@allure.epic("Корзина и заказы")
@allure.feature("API Корзины")
@allure.title("Попытка добавить фейковый товар в реальную корзину")
@pytest.mark.api
@pytest.mark.negative
def test_add_fake_item_to_cart(api_client, empty_cart_id):
    cart_id, pk_key, _, _ = empty_cart_id
    with allure.step("Пробуем добавить несуществующий товар"):
        add_res = api_client.add_item_to_cart(
            cart_id, "variant_fake_hhhhh_222", pk_key=pk_key
        )
        assert add_res.status in [400, 401], "Сервер passed fake item"


@allure.epic("Корзина и заказы")
@allure.feature("API Корзины")
@allure.title("Попытка добавить реальный товар в фейковую корзину")
@pytest.mark.api
@pytest.mark.negative
def test_add_item_to_fake_cart(api_client, generate_product_payload):
    payload = generate_product_payload()
    prod_res = api_client.create_product(payload)
    assert prod_res.status == 200, f"Товар не создался, причина: {prod_res.text()}"
    variant_id = prod_res.json()["product"]["variants"][0]["id"]
    pk_key = api_client.generate_publishable_key()
    with allure.step("Попытка добавить товар в корзину 'fake_fake_fake'"):
        add_res = api_client.add_item_to_cart(
            "fake_fake_fake", variant_id, pk_key=pk_key
        )
        assert add_res.status == 404
    api_client.delete_product(prod_res.json()["product"]["id"])
